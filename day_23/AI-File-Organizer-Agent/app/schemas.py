from pydantic import BaseModel


class OrganizeRequest(BaseModel):
    path: str | None = None


class OrganizeResponse(BaseModel):
    status: str
    files_moved: int
    moved_files: list[str]