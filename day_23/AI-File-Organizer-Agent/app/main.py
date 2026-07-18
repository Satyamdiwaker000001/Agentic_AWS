from fastapi import Body, FastAPI

from app.organizer import organize_folder
from app.schemas import OrganizeRequest, OrganizeResponse

app = FastAPI(
    title="AI File Organizer Agent",
    version="1.0.0",
    description="Automatically organize files into folders."
)
# 

@app.get("/")
def home():
    return {
        "message": "AI File Organizer Agent is Running 🚀"
    }


@app.post("/organize", response_model=OrganizeResponse)
async def organize(body: OrganizeRequest | None = Body(default=None)):
    try:
        if body is None or not body.path:
            raise ValueError("A valid 'path' is required.")

        files_moved, moved_files = organize_folder(body.path)

        return OrganizeResponse(
            status="success",
            files_moved=files_moved,
            moved_files=moved_files
        )
    except Exception as e:
        return OrganizeResponse(
            status="error",
            files_moved=0,
            moved_files=[str(e)]
        )