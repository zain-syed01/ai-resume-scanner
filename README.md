# 🤖 AI Resume Scanner & Recruiter Agent

An end-to-end Retrieval-Augmented Generation (RAG) pipeline built to analyze candidate resumes against job descriptions using vector embeddings and LLM-powered evaluation.

The system indexes resume content into ChromaDB for semantic similarity matching, then leverages Google Gemini to output structured alignment scores, skill gap breakdowns, and actionable bullet-point revisions.

## 🚀 Features

* **PDF Parsing & Extraction:** Extracts raw text from candidate PDF resumes via PyPDF.
* **Metadata Extraction:** Structures candidate name, skills, experience, and summaries using Gemini JSON schemas.
* **Vector Indexing & Semantic Search:** Embeds and stores resume documents in ChromaDB for high-dimensional vector similarity retrieval.
* **Automated Recruiter Evaluation:** Uses Google `gemini-2.5-flash` to evaluate candidate fit, identify skill deficiencies, and suggest tailored resume improvements.
* **Relational Application Tracking:** Tracks application pipelines using PostgreSQL and SQLAlchemy ORM models.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend API:** FastAPI, Uvicorn
* **AI / LLM:** Google Gemini API (`google-genai`)
* **Vector Database:** ChromaDB (Embedded Persistent Client)
* **Relational Database:** PostgreSQL (Neon Serverless), SQLAlchemy
* **Deployment Platforms:** Streamlit Community Cloud (UI), Render (API)

## 🏗️ System Architecture

* **Frontend Layer:** Hosted on Streamlit Community Cloud, providing user session isolation and interactive evaluation rendering.
* **API Layer:** Hosted on Render, managing async endpoints for document ingestion, parsing, and semantic scanning.
* **Database Layer:** 
  * Relational metadata handled via serverless PostgreSQL on Neon.
  * Vector embeddings persisted in embedded local storage via ChromaDB.
* **Payload Handling:** Job descriptions are ingested via structured JSON POST bodies to handle large prompt payloads reliably.

## 💻 Local Setup & Installation

### Prerequisites
* Python 3.10+
* A Google Gemini API Key
* A PostgreSQL Database connection string

### 1. Clone Repository
```bash
git clone [https://github.com/](https://github.com/)<your-username>/ai-resume-scanner.git
cd ai-resume-scanner
2. Environment Variables
Create a .env file in the root directory:

Code snippet
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Run Backend & Frontend
Start the FastAPI backend:

Bash
uvicorn main:app --reload --port 8000
In a separate terminal, start the Streamlit UI:

Bash
streamlit run app.py
📂 Project Structure
Plaintext
├── .env                    # Local environment variables (git-ignored)
├── .gitignore              # Git ignore rules
├── ai_engine.py            # Gemini client & structured metadata extraction
├── app.py                  # Streamlit frontend dashboard
├── database.py             # SQLAlchemy models and database session setup
├── main.py                 # FastAPI endpoints for ingestion and scanning
├── parser.py               # PDF text extraction utilities
├── requirements.txt        # Python dependency declarations
├── schemas.py              # Pydantic data schemas
└── vector_db.py            # ChromaDB persistent collection configuration

---

