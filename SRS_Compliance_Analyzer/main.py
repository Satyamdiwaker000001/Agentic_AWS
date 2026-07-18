import os
import tempfile
from typing import List, Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import existing logic
from parser import parse_document_to_blocks
from analyzer import SRSAnalyzer
from standards import STANDARDS

app = FastAPI(title="SRS Compliance Analyzer API")

# Setup CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
analyzer = SRSAnalyzer()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

@app.get("/api/standards")
def get_standards():
    """Return available standards for the dropdown."""
    return {k: {"title": v["title"], "description": v["description"]} for k, v in STANDARDS.items()}

@app.post("/api/analyze")
async def analyze_document(file: UploadFile = File(...), standard_id: str = "IEEE-830-1998"):
    """Handle document upload and perform compliance analysis."""
    if standard_id not in STANDARDS:
        raise HTTPException(status_code=400, detail="Invalid standard ID")
        
    standard_def = STANDARDS[standard_id]
    
    # Save uploaded file temporarily
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        temp_filepath = tmp_file.name
        
    try:
        # Parse document
        document_blocks = parse_document_to_blocks(temp_filepath)
        total_chars = sum(len(b["text"]) for b in document_blocks)
        
        if total_chars < 100:
            raise HTTPException(status_code=400, detail="Document is too short or has no extractable text.")
            
        # Analyze compliance
        results = analyzer.analyze_compliance(document_blocks, standard_def)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

# AWS Lambda Handler mapping via Mangum
from mangum import Mangum
handler = Mangum(app)
