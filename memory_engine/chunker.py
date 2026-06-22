import logging
import re
from typing import List

logger = logging.getLogger(__name__)

class TextChunker:
    """
    Intelligently splits raw text into smaller, manageable chunks 
    while attempting to respect sentence and paragraph boundaries.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Args:
            chunk_size: The maximum number of characters per chunk.
            chunk_overlap: Approximate character overlap when force-splitting large sentences.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        if self.chunk_size <= self.chunk_overlap:
            raise ValueError("chunk_size must be strictly greater than chunk_overlap.")

    def chunk_text(self, text: str) -> List[str]:
        """
        Splits text into chunks preserving sentence boundaries where possible.
        """
        if not text:
            return []

        # Split into sentences using regex (matches period, question, or exclamation mark followed by space and capital letter)
        sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z0-9])', text)
        
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # If a single sentence is larger than chunk_size, we force-split it
            if len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                start = 0
                while start < len(sentence):
                    end = start + self.chunk_size
                    chunks.append(sentence[start:end])
                    start += (self.chunk_size - self.chunk_overlap)
                continue

            # If adding the next sentence stays within limits, append it
            if len(current_chunk) + len(sentence) + 1 <= self.chunk_size:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                # Chunk is full, save it and start a new one
                chunks.append(current_chunk.strip())
                current_chunk = sentence

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())

        logger.info(f"Intelligently split text into {len(chunks)} chunks.")
        return chunks
