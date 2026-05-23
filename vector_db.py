import os
import chromadb

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8001))

chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def get_or_create_resume_collection():
    """
    Retrieves or creates a vector database collection dedicated to storing
    and indexing resume text chunks.
    """
    try:

        collection = chroma_client.get_or_create_collection(name="resumes")

        return collection
    
    except Exception as e:
        raise Exception(f"Failed to initialize Vector DB collection: {str(e)}")
    
    