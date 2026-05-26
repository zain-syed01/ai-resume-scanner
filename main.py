from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from typing import List
import schemas
from database import JobApplication
from fastapi import UploadFile, File
from parser import extract_text_from_pdf
from ai_engine import analyze_resume_text, client
from vector_db import get_or_create_resume_collection

app = FastAPI(title="Job Application Tracker API")

database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db

    finally:
        db.close()



@app.get("/")
def read_root():
    return {"status": "alive", "message": "Database tables initialized!"}


#Creating Endpoints

@app.post("/apps", response_model=schemas.JobApplicationResponse)
def create_application(app_data: schemas.JobApplicationCreate, db: Session = Depends(get_db)):
    new_app = JobApplication(
        company_name=app_data.company_name,
        job_title=app_data.job_title,
        date_applied=app_data.date_applied,
        status=app_data.status,
        job_url=str(app_data.job_url) if app_data.job_url else None
    )

    db.add(new_app)      
    db.commit()          
    db.refresh(new_app) 
    return new_app

@app.get("/apps", response_model=List[schemas.JobApplicationResponse])
def get_all_applications(db: Session = Depends(get_db)):
    applications = db.query(JobApplication).all()
    return applications


@app.put("/apps/{app_id}", response_model=schemas.JobApplicationResponse)
def update_application(app_id: int, updated_data: schemas.JobApplicationCreate, db: Session = Depends(get_db)):
    db_app = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db_app.company_name = updated_data.company_name
    db_app.job_title = updated_data.job_title
    db_app.date_applied = updated_data.date_applied
    db_app.status = updated_data.status
    db_app.job_url = str(updated_data.job_url) if updated_data.job_url else None

    db.commit()
    db.refresh(db_app)
    return db_app



@app.delete("/apps/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    db_app = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(db_app)
    db.commit()
    return {"message": f"Successfully deleted application with ID {app_id}"}


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        file_bytes = await file.read()
        
        
        resume_text = extract_text_from_pdf(file_bytes)
        
        
        parsed_profile = analyze_resume_text(resume_text)
        
        
        chroma_collection = get_or_create_resume_collection()
        
       
        document_id = f"resume_{file.filename.replace(' ', '_')}"
        
        chroma_collection.upsert(
            documents=[resume_text],
            metadatas=[{"candidate_name": parsed_profile.name, "filename": file.filename}],
            ids=[document_id]
        )
        
        return {
            "filename": file.filename,
            "status": "successfully_parsed_and_indexed",
            "vector_db_id": document_id,
            "extracted_data": parsed_profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing vector upload: {str(e)}")
    

@app.post("/resume/scan")
def scan_resumes_against_job(payload: schemas.JobScanRequest, db: Session = Depends(get_db)):
    """
    Takes a target job description, queries ChromaDB for the most semantically 
    similar resume, and uses Gemini to analyze the gaps.
    """
    job_description = payload.job_description  # Unpack the string from the payload
    try:
        
        chroma_collection = get_or_create_resume_collection()
        
        
        search_results = chroma_collection.query(
            query_texts=[job_description],
            n_results=1
        )
        
       
        if not search_results or not search_results['documents'][0]:
            raise HTTPException(status_code=404, detail="No resumes found in the vector database. Upload a resume first.")
            
        
        matched_resume_text = search_results['documents'][0][0]
        candidate_meta = search_results['metadatas'][0][0]
        candidate_name = candidate_meta.get("candidate_name", "Unknown Candidate")
        
       
        prompt = f"""
        You are an expert AI Technical Recruiter. Compare the candidate's resume against the provided Job Description.
        
        Job Description:
        {job_description}
        
        Candidate's Resume Content:
        {matched_resume_text}
        
        Provide a evaluation containing:
        1. Match Score (0% to 100%) based on semantic skill alignment.
        2. Key Strengths (What matches perfectly).
        3. Skill Gaps (What critical things are missing from the resume).
        4. Bullet Point Improvements (Suggest 2 specific ways the candidate can rewrite their resume bullet points to better match this job description).
        """
        
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return {
            "target_job_description_preview": job_description[:150] + "...",
            "best_matching_candidate": candidate_name,
            "filename": candidate_meta.get("filename"),
            "ai_evaluation": response.text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic scanning failed: {str(e)}")