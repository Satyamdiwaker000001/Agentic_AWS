from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DocumentChunk(BaseModel):
    """Internal model representing a chunk of a document."""
    chunk_id: str
    document_id: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class UploadResponse(BaseModel):
    """Response model for document upload."""
    document_id: str
    num_chunks: int
    status: str
    message: Optional[str] = None

class SearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str
    n_results: int = Field(default=5, ge=1, le=20)

class SearchResult(BaseModel):
    """Model for a single search result."""
    chunk_id: str
    document_id: str
    text: str
    score: float
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    """Response model for semantic search."""
    results: List[SearchResult]
    query: str
    synthesized_answer: Optional[str] = None
