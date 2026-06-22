# SmartChunk AI - Documentation

## 1. What does the project do?
This project is an API-driven document parsing and text chunking engine. It allows users to upload documents of various formats (PDF, DOCX, DOC, TXT), extract their text, and split them using three different chunking algorithms: Fixed Chunker, Recursive Chunker, or Semantic Chunker.

## 2. What is the request flow?
1. **Server Launch**: The backend FastAPI server is started (`uvicorn app:app`).
2. **Client Request**: The client sends a file upload via a POST request to one of the endpoints:
   - `/chunk/fixed`
   - `/chunk/recursive`
   - `/chunk/semantic`
3. **File Buffering**: The uploaded file is saved to the `uploads/` folder.
4. **Text Extraction**: `FileParser` extracts text based on the file extension (using PDF, Word, or RTF parsers).
5. **Chunker Logic Execution**:
   - **Fixed**: Splits text based on character size limits.
   - **Recursive**: Splits text hierarchically using separator delimiters.
   - **Semantic**: Splits text into sentences -> generates embeddings using `all-MiniLM-L6-v2` -> calculates cosine similarity between consecutive sentences. If similarity falls below `similarity_threshold = 0.5` or chunk size exceeds `max_chunk_size = 1500` characters, a new chunk is created.
6. **Response**: Returns a JSON payload containing the chunking method, total chunks count, and the list of text chunks.

## 3. Which packages are used and why?
- **`fastapi` & `uvicorn`**: Provide the REST API endpoints and run the backend server.
- **`sentence-transformers`**: Encodes text sentences into vector embeddings (`all-MiniLM-L6-v2`) for semantic similarity analysis.
- **`scikit-learn`**: Calculates `cosine_similarity` between consecutive sentence vectors.
- **`pypdf` / `docx2txt` / `striprtf`**: Handle text extraction from PDF, DOCX, and RTF files respectively.

## 4. Where does the data come from?
The data comes from files uploaded by the client (via REST endpoints or the React frontend).

## 5. Where is the data stored?
- Upload cache: Uploaded files are temporarily saved to the `uploads/` directory.
- Execution parameters are transient and cleaned up from RAM/disk post response. No persistent database is used.

## 6. What is the role of the LLM?
There is no generative chat LLM. A local embedding model (`all-MiniLM-L6-v2`) is used in the Semantic Chunker to calculate similarities between sentences and determine chunk boundaries.

## 7. What breaks if the LLM is removed?
The Fixed and Recursive chunking endpoints will function perfectly. However, the `/chunk/semantic` endpoint will fail as it depends on `sentence-transformers` embedding calculations.
