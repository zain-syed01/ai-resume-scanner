import chromadb

# Uses an embedded, persistent Chroma client stored locally inside the container
chroma_client = chromadb.PersistentClient(path="./chroma_db")

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