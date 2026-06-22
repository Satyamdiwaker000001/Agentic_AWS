import logging
import chromadb
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class MemoryStore:
    """
    Handles persistence and retrieval of vector embeddings using ChromaDB.
    """

    def __init__(self, db_dir: str | Path, collection_name: str = "memory_engine"):
        self.db_dir = str(db_dir)
        self.client = chromadb.PersistentClient(path=self.db_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        logger.info(f"Initialized MemoryStore at {self.db_dir} with collection '{collection_name}'")

    def document_exists(self, file_hash: str) -> bool:
        """
        Checks if a document with the given hash already exists in the store.
        """
        results = self.collection.get(
            where={"file_hash": file_hash},
            limit=1
        )
        return len(results.get("ids", [])) > 0

    def add_chunks(
        self, 
        ids: List[str], 
        embeddings: List[List[float]], 
        documents: List[str], 
        metadatas: List[Dict[str, Any]]
    ) -> None:
        """
        Adds text chunks, their embeddings, and metadata to the vector store.
        """
        if not ids:
            return

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        logger.debug(f"Added {len(ids)} chunks to the memory store.")

    def search(self, query_embedding: List[float], n_results: int = 5) -> Dict[str, Any]:
        """
        Searches the vector store for the closest chunks to the query embedding.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

    def health(self) -> str:
        """Checks if the ChromaDB client is responsive."""
        try:
            self.client.heartbeat()
            return "healthy"
        except Exception as e:
            logger.error(f"ChromaDB health check failed: {e}")
            return "unhealthy"
