# Embedding Memory Agent - Documentation

## 1. What does the project do?
This project is a local semantic memory storage and retrieval agent. It allows users to store textual descriptions/memories and retrieve the most semantically relevant memory block when queried.

## 2. What is the request flow?
1. **Interactive Menu**: The user runs `main.py` and is presented with options to Save Memory, Search Memory, or Exit.
2. **Save Memory Flow**:
   - The user inputs a sentence.
   - `MemoryManager` appends the string to `data/memory.txt`.
   - `Retriever` fetches all saved sentences, and `EmbeddingModel` computes their vector representations using the `all-MiniLM-L6-v2` model.
   - The generated float vectors are serialized and saved to `embeddings/memory_vectors.pkl` using pickle.
3. **Search Memory Flow**:
   - The user inputs a query.
   - The query text is encoded into a float vector.
   - The saved float vectors are loaded from the pickle database.
   - The cosine similarity score is calculated between the query vector and all saved vectors.
   - The index of the highest similarity score is retrieved, and the corresponding memory sentence is printed to the console.

## 3. Which packages are used and why?
- **`sentence-transformers`**: Provides the `all-MiniLM-L6-v2` model to encode raw texts into semantic vector coordinates.
- **`scikit-learn`**: Used to compute the `cosine_similarity` metric between vectors.
- **`pickle` (standard library)**: Used for serializing/deserializing vector arrays to local files.
- **`os` (standard library)**: Handles path operations and ensures necessary directories exist.

## 4. Where does the data come from?
The data comes from user keyboard inputs entered in the terminal console at runtime.

## 5. Where is the data stored?
- Raw texts: `data/memory.txt`
- Compiled vector embeddings: `embeddings/memory_vectors.pkl`

## 6. What is the role of the LLM?
There is no generative chat LLM. Instead, a lightweight embedding model (`sentence-transformers/all-MiniLM-L6-v2`) is used to convert textual data into mathematical vector coordinates to perform semantic matching.

## 7. What breaks if the LLM is removed?
If the sentence-transformer package or model is removed, the vector calculations will fail, and semantic search (Choice 2) will break. The system would need a fallback search method based on keyword/regex substring matching.
