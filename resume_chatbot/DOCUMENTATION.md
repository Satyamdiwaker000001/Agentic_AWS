# Resume Chatbot - Documentation

## 1. What does the project do?
This project is an interactive resume search chatbot. It extracts text from a local PDF resume (`resume.pdf`), splits it into chunks, embeds them, indexes them in a local FAISS vector store, and hosts a web UI using Gradio to let users search the resume.

## 2. What is the request flow?
1. **Model Loading & Indexing**:
   - The user runs `app.py`.
   - Text is extracted from `resume.pdf` using `pypdf.PdfReader`.
   - The text is split into chunks of 500 characters using `chunk_text()`.
   - The embedding model `all-MiniLM-L6-v2` encodes all chunks into float arrays.
   - An in-memory FAISS L2 index is created, and the chunk embeddings are added to it.
2. **Gradio UI Launch**: The Gradio web interface launches locally.
3. **Query Processing**:
   - The user types a query in the text input box.
   - The query is encoded using the embedding model.
   - FAISS searches the index to retrieve the top `k=3` closest resume chunks.
   - The retrieved chunks are joined and displayed in the Gradio output textbox.

## 3. Which packages are used and why?
- **`pypdf`**: Used to extract text content from the input PDF resume.
- **`sentence-transformers`**: Provides the embedding model (`all-MiniLM-L6-v2`) to compute text vector representations.
- **`faiss-cpu`**: Handles local vector storage, indexing, and similarity searches.
- **`numpy`**: Converts python list embeddings to float32 numpy arrays for FAISS.
- **`gradio`**: Implements the web interface with input/output text boxes.

## 4. Where does the data come from?
- Resume profiles: PDF file `resume.pdf`.
- User search queries: Entered in the Gradio UI text box.

## 5. Where is the data stored?
All evaluations, vector encodings, and the FAISS index are stored dynamically in RAM variables. No persistent database or files are saved on disk.

## 6. What is the role of the LLM?
There is no generative chat LLM. Instead, a lightweight embedding model (`sentence-transformers/all-MiniLM-L6-v2`) is used to convert textual descriptions into vector coordinate structures to perform mathematical similarity matching.

## 7. What breaks if the LLM is removed?
If the sentence-transformer packages or model is removed, the vector calculations will fail, and semantic search queries will break. The system would need a fallback search method based on keyword/regex substring matching.
