from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resume

app = FastAPI(title="ResumePilot AI Backend")

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api", tags=["resume"])

@app.get("/")
def read_root():
    return {"message": "Welcome to ResumePilot AI API"}
