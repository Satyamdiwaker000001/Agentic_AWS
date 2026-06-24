import time
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import tempfile
import os

# ─── Import graph EARLY so model loads at import time ──────────────
# The Qwen model loads inside models/qwen_model.py at module level.
# By importing graph here, the model is loaded ONCE when server starts.
from graph import graph


@asynccontextmanager
async def lifespan(app):
    """Runs at server startup — model is already loaded by import above."""
    print("[OK] Server ready! Model is preloaded and warmed up.")
    print("[>>] API available at http://127.0.0.1:8000/api/chat")
    yield
    print("[--] Server shutting down...")


app = FastAPI(title="Nexus AI Workspace API", lifespan=lifespan)

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    intent: str
    agent: str
    confidence: float
    response: str
    metadata: dict

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        start_time = time.time()
        
        # Invoke the LangGraph graph
        result = graph.invoke({
            "message": req.message
        })
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        intent = result.get("task_type", "general")
        confidence = result.get("confidence", 0.90)
        response_text = result.get("response", "No response generated.")
        agent_metadata = result.get("metadata", {})
        
        # Map intent to readable agent name
        agent_names = {
            "general": "General Agent",
            "coding": "Coding Agent",
            "debug": "Debug Agent",
            "math": "Math Agent",
            "physics": "Physics Agent"
        }
        agent_name = agent_names.get(intent, "General Agent")
        
        # Calculate mock tokens
        tokens_map = {
            "general": random.randint(40, 80),
            "coding": random.randint(250, 450),
            "debug": random.randint(180, 350),
            "math": random.randint(120, 240),
            "physics": random.randint(110, 220)
        }
        tokens_used = tokens_map.get(intent, 50)
        
        # Combine backend processing metadata
        response_metadata = {
            **agent_metadata,
            "responseTime": response_time,
            "agentUsed": agent_name,
            "tokensUsed": tokens_used,
            "stage": "Response Generation"
        }
        
        return ChatResponse(
            intent=intent,
            agent=agent_name,
            confidence=confidence,
            response=response_text,
            metadata=response_metadata
        )
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class RunRequest(BaseModel):
    language: str
    code: str

class RunResponse(BaseModel):
    stdout: str
    stderr: str
    exitCode: int

@app.post("/api/run", response_model=RunResponse)
async def run_code(req: RunRequest):
    ext_map = {
        "python": ".py",
        "javascript": ".js",
        "node": ".js",
        "java": ".java",
        "html": ".html"
    }
    ext = ext_map.get(req.language.lower(), ".txt")
    
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(req.code)
        temp_path = temp_file.name

    try:
        cmd = []
        lang = req.language.lower()
        if lang == "python":
            cmd = ["python", temp_path]
        elif lang in ["javascript", "node"]:
            cmd = ["node", temp_path]
        elif lang == "java":
            # For Java, we really need the class name, but we will fallback to simple error
            return RunResponse(stdout="", stderr="Java execution requires Classname alignment. Not supported in quick preview.", exitCode=1)
        else:
            return RunResponse(stdout="", stderr=f"Backend execution for language '{req.language}' is not implemented.", exitCode=1)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return RunResponse(
            stdout=result.stdout,
            stderr=result.stderr,
            exitCode=result.returncode
        )
    except subprocess.TimeoutExpired:
        return RunResponse(stdout="", stderr="Execution timed out after 10 seconds.", exitCode=124)
    except Exception as e:
        return RunResponse(stdout="", stderr=str(e), exitCode=1)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/api/dashboard/stats")
async def dashboard_stats_endpoint():
    # Return stats dashboard information matching requirements
    return {
        "totalQueries": 1284,
        "codingQueries": 487,
        "mathQueries": 352,
        "physicsQueries": 214,
        "debugQueries": 231,
        "activity": [
            {"day": "Mon", "queries": 145},
            {"day": "Tue", "queries": 182},
            {"day": "Wed", "queries": 160},
            {"day": "Thu", "queries": 210},
            {"day": "Fri", "queries": 245},
            {"day": "Sat", "queries": 190},
            {"day": "Sun", "queries": 152}
        ],
        "agentUsage": [
            {"name": "General AI", "value": 310},
            {"name": "Coding Agent", "value": 487},
            {"name": "Math Agent", "value": 352},
            {"name": "Physics Agent", "value": 214},
            {"name": "Debug Agent", "value": 231}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
