import streamlit as st
import requests
import os

# Set page configuration
st.set_page_config(page_title="AI Resume Scanner", page_icon="💼", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🤖 AI RAG Resume Scanner & Recruiter Agent")
st.write("Upload a resume and paste a job description to analyze semantic alignment and get structural feedback.")

# Create two clean columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Submit Candidate Document")
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("🚀 Parse & Index Resume"):
            with st.spinner("Extracting text and generating vector embeddings..."):
                try:
                    # Prepare the file payload for FastAPI
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    
                    # Hit our FastAPI container upload endpoint
                    response = requests.post(f"{BACKEND_URL}/resume/upload", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Successfully processed {data['filename']}!")
                        st.json(data["extracted_data"]) # Show the clean JSON structural data
                    else:
                        st.error(f"Backend returned an error: {response.text}")
                except Exception as e:
                    st.error(f"Could not connect to backend pipeline: {e}")

with col2:
    st.subheader("2. Run AI Semantic Scan")
    job_description = st.text_area("Paste Target Job Description Here", height=250, placeholder="Looking for a software engineer proficient in Python, FastAPI, and Docker...")
    
    if st.button("🔍 Analyze Job Alignment"):
        if not job_description:
            st.warning("Please paste a job description first.")
        else:
            with st.spinner("Querying ChromaDB and invoking Gemini engine..."):
                try:
                    # Pass the job description text as a query parameter to our scan route
                    payload = {"job_description": job_description}
                    response = requests.post(f"{BACKEND_URL}/resume/scan", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.balloons()
                        
                        st.markdown("---")
                        st.subheader(f"🎯 Best Matching Candidate: {result['best_matching_candidate']}")
                        st.caption(f"Source file: {result['filename']}")
                        
                        st.markdown("### 📋 AI Recruiter Evaluation")
                        # Because Gemini outputs pure Markdown, Streamlit renders it beautifully!
                        st.markdown(result["ai_evaluation"])
                    else:
                        st.error(f"Backend evaluation failed: {response.text}")
                except Exception as e:
                    st.error(f"Could not connect to backend engine: {e}")