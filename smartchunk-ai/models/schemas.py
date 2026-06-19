from pydantic import BaseModel


class ChunkResponse(BaseModel):

    method: str
    total_chunks: int
    chunks: list[str]