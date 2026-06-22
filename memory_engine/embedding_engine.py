import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingEngine:
    """
    Generates vector embeddings for text using SentenceTransformers.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the embedding model.

        Args:
            model_name: The HuggingFace sentence-transformers model name.
        """
        self.model_name = model_name
        logger.info(f"Loading embedding model: {self.model_name}")
        # Initialize the model on startup to prevent latency on first request
        self.model = SentenceTransformer(self.model_name)
        logger.info("Embedding model loaded successfully.")

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates vector embeddings for a list of text strings.

        Args:
            texts: A list of string texts to embed.

        Returns:
            A list of vector embeddings (lists of floats).
        """
        if not texts:
            return []

        logger.debug(f"Generating embeddings for {len(texts)} texts.")
        # encode returns a numpy array, we convert to list for generic Python usage/ChromaDB
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
