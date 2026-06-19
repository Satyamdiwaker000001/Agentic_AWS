"""Generic file parser that routes to the appropriate parser based on file type."""

from parsers.pdf_parser import PDFParser
from parsers.text_parser import TXTParser
from parsers.docx_parser import DOCXParser
from parsers.doc_parser import DOCParser


class FileParser:
    """Routes file parsing to the appropriate parser based on file extension."""
    
    PARSERS = {
        '.pdf': PDFParser,
        '.txt': TXTParser,
        '.docx': DOCXParser,
        '.doc': DOCParser,
    }
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from any supported file type.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file type is not supported
        """
        import os
        
        # Get file extension and convert to lowercase
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Get the appropriate parser
        parser_class = FileParser.PARSERS.get(ext)
        
        if parser_class is None:
            supported = ', '.join(FileParser.PARSERS.keys())
            raise ValueError(
                f"Unsupported file type '{ext}'. Supported types: {supported}"
            )
        
        # Extract and return text
        return parser_class.extract_text(file_path)
    
    @staticmethod
    def get_supported_types():
        """Return list of supported file extensions."""
        return list(FileParser.PARSERS.keys())
