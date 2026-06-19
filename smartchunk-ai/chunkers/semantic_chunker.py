import re
from typing import List
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticChunker:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", similarity_threshold: float = 0.5, max_chunk_size: int = 1500):
        """
        Initialize the Semantic Chunker.
        
        Args:
            model_name: The sentence-transformers model to use.
            similarity_threshold: Cosine similarity threshold below which sentences are split into new chunks.
            max_chunk_size: Maximum character limit for a chunk before forcing a split.
        """
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold
        self.max_chunk_size = max_chunk_size

    def _split_into_sentences(self, text: str) -> List[str]:
        # Simple regex based sentence splitting
        text = text.replace('\n', ' ').strip()
        if not text:
            return []
        # Split by . ! ? followed by space and a capital letter
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [s.strip() for s in sentences if s.strip()]

    def chunk(self, text: str) -> List[str]:
        sentences = self._split_into_sentences(text)
        if not sentences:
            return []
        
        if len(sentences) == 1:
            return sentences

        # Generate embeddings for all sentences
        embeddings = self.model.encode(sentences)

        chunks = []
        current_chunk = sentences[0]
        current_embedding = embeddings[0]

        for i in range(1, len(sentences)):
            sentence = sentences[i]
            embedding = embeddings[i]

            # Calculate cosine similarity between current chunk representation and next sentence
            # Reshape for sklearn
            sim = cosine_similarity(current_embedding.reshape(1, -1), embedding.reshape(1, -1))[0][0]

            candidate_chunk = current_chunk + " " + sentence

            # If the semantic similarity is below threshold OR the chunk becomes too large
            if sim < self.similarity_threshold or len(candidate_chunk) > self.max_chunk_size:
                chunks.append(current_chunk)
                current_chunk = sentence
                current_embedding = embedding
            else:
                current_chunk = candidate_chunk
                # Update current embedding to be the average of the sentences in it (simple approximation)
                current_embedding = (current_embedding + embedding) / 2.0

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
