import os
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types


client = genai.Client()

class ExtractedResumeData(BaseModel):
    name: str
    skills: List[str]
    experience_years: int
    education: List[str]
    summary: str



def analyze_resume_text(resume_text: str) -> ExtractedResumeData:
    """
    Sends raw resume text to Gemini and forces it to extract key metadata
    as a structured JSON object matching our Pydantic schema.
    """
    prompt = f"""
    You are an expert technical recruiter parsing a candidate's resume text.
    Extract the candidate's name, core technical skills, total years of relevant professional experience, 
    education background, and a 2-sentence summary of their profile.
    
    Raw Resume Text:
    \"\"\"{resume_text}\"\"\"
    """


    try:
        response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ExtractedResumeData,
                    temperature=0.1
                ),
        )

        return ExtractedResumeData.model_validate_json(response.text)
    except Exception as e:
            raise Exception(f"Gemini processing failed: {str(e)}")