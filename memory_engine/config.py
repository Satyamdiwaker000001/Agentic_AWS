import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings for the Memory Engine AI Phase 1.
    Reads from environment variables or uses default values.
    """
    
    # Project Paths
    base_dir: Path = Path(__file__).resolve().parent
    upload_dir: Path = base_dir / "uploads"
    chroma_db_dir: Path = base_dir / "chroma_db"
    
    # Vector Database / Embedding Configuration
    embedding_model_name: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def setup_directories(self) -> None:
        """Ensure necessary directories exist."""
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.chroma_db_dir, exist_ok=True)


# Initialize global settings
settings = Settings()
settings.setup_directories()
