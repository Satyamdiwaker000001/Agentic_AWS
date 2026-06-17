from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
import shutil
import os
from app.services.analyzer import analyze_resume

router = APIRouter()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AnalyzeResponse(BaseModel):
    score: int
    findings: dict
    radarData: list
    scoreBreakdown: list
    roleMatch: dict

@router.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.txt', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF, TXT or DOCX files are supported for JD.")
        
    file_path = os.path.join(UPLOAD_DIR, f"jd_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Here we would typically extract text from the file
        # Mock extracted text for now
        extracted_text = f"Extracted text from {file.filename}..."
        
        return {"filename": file.filename, "extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score")
async def score_resume(
    resumeFile: UploadFile = File(...),
    jdText: str = Form(...)
):
    if not resumeFile.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for resume.")
        
    file_path = os.path.join(UPLOAD_DIR, resumeFile.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resumeFile.file, buffer)
            
        # Mock simple scoring for this separate API
        results = analyze_resume(file_path, "Custom Job", jdText)
        
        return {
            "score": results["score"],
            "roleMatch": results["roleMatch"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    jobTitle: str = Form(...),
    jobDescription: str = Form(...)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Call the analyzer service (mocked for now)
        results = analyze_resume(file_path, jobTitle, jobDescription)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up file if needed
        if os.path.exists(file_path):
            os.remove(file_path)
