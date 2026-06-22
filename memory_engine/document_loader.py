import fitz  # PyMuPDF
import logging
import hashlib
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)

class DocumentLoader:
    """
    Handles extracting text and metadata from documents.
    """

    @staticmethod
    def compute_hash(file_path: str | Path) -> str:
        """Computes the SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def load_pdf(file_path: str | Path) -> Tuple[str, str]:
        """
        Extracts text from a PDF and computes its hash.

        Args:
            file_path: The path to the PDF file.

        Returns:
            Tuple containing (extracted_text, file_hash).
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file cannot be opened or parsed.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found at {path}")

        try:
            file_hash = DocumentLoader.compute_hash(path)
            
            doc = fitz.open(path)
            text_blocks = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text:
                    text_blocks.append(text)
                else:
                    logger.warning(f"No text extracted from page {page_num + 1} of {path.name}")
                    
            doc.close()
            return "\n".join(text_blocks), file_hash
            
        except Exception as e:
            logger.error(f"Failed to process PDF {path}: {str(e)}")
            raise ValueError(f"Could not process PDF document: {str(e)}")
