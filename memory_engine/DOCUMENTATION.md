# Memory Engine - Documentation

## 1. What does the project do?
This project is an API-driven AI Second Brain system. It allows users to upload PDF documents, extract their text, split them into chunks, generate vector embeddings, and store them in a local persistent database. Users can perform semantic searches over the stored documents and receive intelligent conversational responses synthesized via the Groq API.

## 2. What is the request flow?
1. **API Initialization**: FastAPI starts up, setups directories, and instantiates singletons (chunker, embedding engine, ChromaDB client, agent layer).
2. **Upload Endpoint (`/upload`)**:
   - The user uploads a PDF.
   - The server verifies it is a PDF.
   - Text extraction and MD5 hashing run in a background thread to prevent event-loop blocking (`DocumentLoader`).
   - The script checks if the file hash already exists to prevent duplicate processing.
   - Text is split into overlapping chunks using `TextChunker`.
   - Embeddings are generated using `EmbeddingEngine` (loaded with `all-MiniLM-L6-v2`).
   - The chunk texts, embeddings, and metadata are saved to a local Chroma database.
3. **Search Endpoint (`/search`)**:
   - The user submits a query string.
   - `SearchEngine` queries the Chroma database to fetch the top `n_results=5` matching snippets.
   - `AgentLayer` compiles the snippets into a prompt.
   - A completions request is sent to the Groq API client loading `llama3-8b-8192`.
   - The synthesized response is returned to the user as JSON.

## 3. Which packages are used and why?
- **`fastapi` & `uvicorn`**: Provide the REST API endpoints and run the backend server.
- **`chromadb`**: Local persistent vector database to store and query document chunk embeddings.
- **`sentence-transformers`**: Generates vector representations of text segments.
- **`groq`**: Integrates Groq cloud completions API for low-latency conversational response synthesis.
- **`pydantic-settings`**: Automatically binds configurations and API keys from a local `.env` file.
- **`starlette`** (`run_in_threadpool`): Runs CPU-heavy tasks (hashing, text chunking, local embeddings) in a separate thread pool.

## 4. Where does the data come from?
- Input documents: Uploaded via `/upload` REST requests.
- Queries: Input query parameters sent via `/search` requests.

## 5. Where is the data stored?
- Raw files cache: Saved temporarily under the `uploads/` directory.
- Database index: Persisted in the `chroma_db/` directory.

## 6. What is the role of the LLM?
The system utilizes two types of models:
1. Local embedding model (`all-MiniLM-L6-v2`): Converts text inputs into float arrays.
2. Cloud LLM (`llama3-8b-8192` via Groq client): Reads retrieved context fragments to answer the user query accurately and conversationally.

## 7. What breaks if the LLM is removed?
If local embedding libraries are removed, both document indexing and searches will crash. If the Groq connection is disabled, `/search` will still return raw matching text snippets but will not be able to generate conversational answers.
