
import chromadb
import uuid
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
            self.collection = self.client.get_or_create_collection(name="error_fixes")
            logger.info(f"VectorStore connected to {settings.CHROMA_DB_DIR}")
        except Exception as e:
            logger.error(f"Failed to initialize VectorStore: {e}")
            self.collection = None

    def add_record(self, error: str, code: str, fix: str):
        if not self.collection:
            return
        
        try:
            self.collection.add(
                documents=[error],
                metadatas=[{"code_snippet": code[:200], "fix": fix}],
                ids=[str(uuid.uuid4())]
            )
        except Exception as e:
            logger.error(f"Error adding record to VectorDB: {e}")

    def search_similar_error(self, error: str, n_results: int = 1):
        if not self.collection:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[error],
                n_results=n_results
            )
            if results and results['documents']:
                return [
                    {
                        "error": doc,
                        "fix": meta.get("fix")
                    }
                    for doc, meta in zip(results['documents'][0], results['metadatas'][0])
                ]
            return []
        except Exception as e:
            logger.error(f"Error querying VectorDB: {e}")
            return []
