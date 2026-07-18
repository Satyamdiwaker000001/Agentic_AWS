from fastapi import Body, FastAPI
from pydantic import BaseModel
import os
import shutil

app = FastAPI()

class OrganizeRequest(BaseModel):
    path: str | None = None

@app.get("/")
def home():
    return {"message": "Simple File Organizer is running"}

@app.post("/organize")
async def organize(body: OrganizeRequest | None = Body(default=None)):
    if body is None or not body.path:
        return {"status": "error", "message": "Please send a valid 'path' field"}

    folder = body.path

    if not os.path.exists(folder):
        return {"status": "error", "message": "Folder not found"}

    if not os.path.isdir(folder):
        return {"status": "error", "message": "This is not a folder"}

    moved = []
    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)
        if os.path.isdir(full_path):
            continue

        ext = os.path.splitext(item)[1].lower()
        if ext in {".txt", ".md", ".py"}:
            category = "Documents"
        elif ext in {".jpg", ".png", ".jpeg"}:
            category = "Images"
        else:
            category = "Others"

        target_folder = os.path.join(folder, category)
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(full_path, os.path.join(target_folder, item))
        moved.append(item)

    return {"status": "success", "moved_files": moved}
