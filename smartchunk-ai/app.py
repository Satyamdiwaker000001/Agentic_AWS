from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

import os

from parsers.file_parser import FileParser
from chunkers.fixed_chunker import FixedChunker
from chunkers.recursive_chunker import RecursiveChunker
from chunkers.semantic_chunker import SemanticChunker

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SmartChunk AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message": "SmartChunk AI Running"
    }


@app.post("/chunk/fixed")
async def fixed_chunking(
    file: UploadFile = File(...)
):

    filename = file.filename or "uploaded_file.txt"

    path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        text = FileParser.extract_text(path)
    except ValueError as e:
        return {
            "error": str(e),
            "supported_types": FileParser.get_supported_types()
        }

    chunker = FixedChunker()

    chunks = chunker.chunk(text)

    return {
        "method": "fixed",
        "total_chunks": len(chunks),
        "chunks": chunks
    }


@app.post("/chunk/recursive")
async def recursive_chunking(
    file: UploadFile = File(...)
):

    filename = file.filename or "uploaded_file.txt"

    path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        text = FileParser.extract_text(path)
    except ValueError as e:
        return {
            "error": str(e),
            "supported_types": FileParser.get_supported_types()
        }

    chunker = RecursiveChunker()

    chunks = chunker.chunk(text)

    return {
        "method": "recursive",
        "total_chunks": len(chunks),
        "chunks": chunks
    }

@app.post("/chunk/semantic")
async def semantic_chunking(
    file: UploadFile = File(...)
):

    filename = file.filename or "uploaded_file.txt"

    path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        text = FileParser.extract_text(path)
    except ValueError as e:
        return {
            "error": str(e),
            "supported_types": FileParser.get_supported_types()
        }

    chunker = SemanticChunker()

    chunks = chunker.chunk(text)

    return {
        "method": "semantic",
        "total_chunks": len(chunks),
        "chunks": chunks
    }