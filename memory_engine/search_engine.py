import logging
from typing import List
from embedding_engine import EmbeddingEngine
from memory_store import MemoryStore
from models import SearchResult

logger = logging.getLogger(__name__)

class SearchEngine:
    """
    Orchestrates the semantic search process.
    It takes a query, generates its embedding, and fetches the most relevant chunks from the MemoryStore.
    """

    def __init__(self, embedding_engine: EmbeddingEngine, memory_store: MemoryStore):
        self.embedding_engine = embedding_engine
        self.memory_store = memory_store

    def search(self, query: str, n_results: int = 5) -> List[SearchResult]:
        """
        Executes a semantic search.

        Args:
            query: The user's search string.
            n_results: Maximum number of results to retrieve.

        Returns:
            A list of SearchResult objects containing the relevant chunks and their scores.
        """
        if not query.strip():
            return []

        # 1. Generate embedding for the query
        logger.debug(f"Generating embedding for search query: '{query}'")
        query_embeddings = self.embedding_engine.generate_embeddings([query])
        
        if not query_embeddings:
            return []
            
        query_embedding = query_embeddings[0]

        # 2. Search the memory store
        raw_results = self.memory_store.search(query_embedding=query_embedding, n_results=n_results)

        # 3. Parse and return results
        search_results = []
        
        # ChromaDB returns lists of lists since it supports batched queries.
        # We only queried a single embedding, so we access index 0.
        if not raw_results or not raw_results.get("ids") or not raw_results["ids"][0]:
            return search_results

        ids = raw_results["ids"][0]
        distances = raw_results.get("distances", [[0.0]])[0]
        documents = raw_results.get("documents", [[""]])[0]
        metadatas = raw_results.get("metadatas", [[{}]])[0]

        for i in range(len(ids)):
            search_results.append(
                SearchResult(
                    chunk_id=ids[i],
                    document_id=metadatas[i].get("document_id", "unknown"),
                    text=documents[i],
                    score=distances[i],  # In ChromaDB (using default L2), lower distance is better.
                    metadata=metadatas[i]
                )
            )

        logger.info(f"Found {len(search_results)} results for query: '{query}'")
        return search_results
