import uuid
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool
from contextlib import asynccontextmanager

from config import settings
from models import UploadResponse, SearchResponse
from document_loader import DocumentLoader
from chunker import TextChunker
from embedding_engine import EmbeddingEngine
from memory_store import MemoryStore
from search_engine import SearchEngine
from agent_layer import AgentLayer
from dependencies import get_chunker, get_embedding_engine, get_memory_store, get_search_engine, get_agent_layer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Enterprise Memory Engine components...")
    settings.setup_directories()
    
    # Pre-initialize singletons
    get_chunker()
    get_embedding_engine()
    get_memory_store()
    get_search_engine()
    get_agent_layer()
    
    logger.info("Enterprise Memory Engine ready.")
    yield
    logger.info("Shutting down Memory Engine...")

app = FastAPI(
    title="Memory Engine AI (Enterprise Edition)",
    description="An advanced, industry-friendly API for an AI Second Brain",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static frontend
import os
os.makedirs("static", exist_ok=True)
app.mount("/app", StaticFiles(directory="static", html=True), name="static")

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "error": str(exc)}
    )

@app.get("/health")
async def health_check(memory_store: MemoryStore = Depends(get_memory_store)) -> Dict[str, Any]:
    """Check the health of the API and connected services."""
    return {
        "status": "online",
        "chromadb": memory_store.health(),
        "version": "1.0.0"
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunker: TextChunker = Depends(get_chunker),
    embedding_engine: EmbeddingEngine = Depends(get_embedding_engine),
    memory_store: MemoryStore = Depends(get_memory_store)
):
    """
    Upload a PDF document.
    Extracts text, chunks it, generates embeddings, and stores in ChromaDB.
    Runs CPU-bound tasks in a threadpool to prevent event loop blocking.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    document_id = str(uuid.uuid4())
    file_path = settings.upload_dir / f"{document_id}.pdf"
    
    try:
        # Save file to disk
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract text and compute hash (CPU Bound)
        text, file_hash = await run_in_threadpool(DocumentLoader.load_pdf, file_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF.")

        # Check for deduplication
        if memory_store.document_exists(file_hash):
            logger.info(f"Document {file.filename} already exists. Skipping processing.")
            return UploadResponse(
                document_id="existing",
                num_chunks=0,
                status="skipped",
                message="Document already exists in the system."
            )

        # Chunk text (CPU Bound)
        chunks = await run_in_threadpool(chunker.chunk_text, text)
        
        # Generate embeddings (CPU Bound - ML Model)
        embeddings = await run_in_threadpool(embedding_engine.generate_embeddings, chunks)

        # Prepare for storage
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {"document_id": document_id, "filename": file.filename, "file_hash": file_hash} 
            for _ in range(len(chunks))
        ]

        # Store in ChromaDB (I/O Bound)
        await run_in_threadpool(
            memory_store.add_chunks,
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        return UploadResponse(
            document_id=document_id,
            num_chunks=len(chunks),
            status="success",
            message="Document processed and stored successfully."
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search", response_model=SearchResponse)
async def search_memory(
    query: str, 
    n_results: int = 5,
    search_engine: SearchEngine = Depends(get_search_engine),
    agent_layer: AgentLayer = Depends(get_agent_layer)
):
    """
    Semantic search over stored documents, enriched with an AI-synthesized answer.
    """
    try:
        # 1. Retrieve raw chunks
        results = await run_in_threadpool(search_engine.search, query=query, n_results=n_results)
        
        # 2. Synthesize answer using the Agent Layer
        synthesized_answer = await run_in_threadpool(agent_layer.synthesize_answer, query, results)
        
        return SearchResponse(
            query=query,
            results=results,
            synthesized_answer=synthesized_answer
        )
    except Exception as e:
        logger.error(f"Error performing search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
