Markdown
# 🤖 AI Resume Scanner & Recruiter Agent

An end-to-end, fully Dockerized Retrieval-Augmented Generation (RAG) pipeline built to analyze resumes against target job descriptions. 

This application uses semantic vector search to find the best candidate for a role and leverages the Google Gemini AI engine to generate comprehensive recruiter evaluations, including match scores, skill gaps, and resume improvement suggestions.

## 🚀 Features

* **PDF Parsing & Extraction:** Securely uploads and extracts raw text from candidate PDF resumes.
* **Vector Database Indexing:** Chunks and embeds resume data into a persistent ChromaDB vector store for semantic searching.
* **AI Semantic Job Alignment:** Compares target job descriptions against the vector database to find the most semantically aligned candidate profile.
* **Automated Recruiter Feedback:** Utilizes Google's `gemini-2.5-flash` model to generate actionable feedback, highlighting strengths, missing critical skills, and bullet-point rewrite suggestions.
* **Secure Multi-Container Architecture:** Completely isolated backend network layers preventing unauthorized public access to databases and APIs.

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Python)
* **Backend API:** FastAPI, Uvicorn
* **AI / LLM:** Google Gemini API (`genai`)
* **Vector Database:** ChromaDB
* **Relational Database:** PostgreSQL, SQLAlchemy
* **Deployment & Infrastructure:** Docker Compose, AWS EC2 (Ubuntu)

## 🏗️ System Architecture & Security

This project was built with production-grade network isolation. 
* The application runs on an AWS EC2 instance managed via **Docker Compose**.
* **Public Access:** Only the Streamlit Frontend (Port `8501`) is exposed to the public internet via AWS Security Groups.
* **Private Network:** The FastAPI backend, PostgreSQL database, and ChromaDB vector store exist entirely on a closed, internal Docker bridge network. The frontend communicates with the backend exclusively through internal Docker DNS (e.g., `http://web:8000`), bypassing the public internet entirely.
* **Data Handling:** Large text payloads (like 500+ word Job Descriptions) are routed securely via JSON body payloads rather than URI parameters to prevent buffer overflow limits.

## 💻 Local Setup & Installation

### Prerequisites
* [Docker](https://www.docker.com/products/docker-desktop) and Docker Compose installed.
* A [Google Gemini API Key](https://aistudio.google.com/).

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/ai-resume-scanner.git](https://github.com/yourusername/ai-resume-scanner.git)
cd ai-resume-scanner
2. Configure Environment Variables
Create a .env file in the root directory and add your API key. (Note: This file is git-ignored for security).

Code snippet
GEMINI_API_KEY=your_actual_api_key_here
3. Build and Spin Up the Containers
Use Docker Compose to build the images and start the isolated network grid in the background:

Bash
docker compose up -d --build
4. Access the Application
Frontend UI: Open your browser and navigate to http://localhost:8501

Backend API Docs (Swagger): Navigate to http://localhost:8000/docs

📂 Project Structure
Plaintext
├── .env                    # Hidden environment variables
├── .gitignore              # Git ignore rules
├── ai_engine.py            # Gemini API integration and JSON schema validation
├── app.py                  # Streamlit frontend dashboard
├── database.py             # PostgreSQL connection and SQLAlchemy schema
├── docker-compose.yml      # Multi-container orchestration and networking
├── Dockerfile              # Container build instructions
├── main.py                 # FastAPI backend routes
├── parser.py               # PyPDF text extraction logic
├── requirements.txt        # Python dependencies
├── schemas.py              # Pydantic data validation models
└── vector_db.py            # ChromaDB initialization and collections
🛑 Stopping the Application
To safely spin down the containers and preserve your database volumes:

Bash
docker compose down
