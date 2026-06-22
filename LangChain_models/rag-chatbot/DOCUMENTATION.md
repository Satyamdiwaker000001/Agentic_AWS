# LangChain RAG Chatbot - Documentation

## 1. What does the project do?
This project is an interactive web-based document QA assistant built with Streamlit and LangChain. It allows users to upload a document (PDF, TXT, or DOCX), index its contents, and chat with it by asking contextual questions. The chatbot responds strictly based on the content of the uploaded document.

## 2. What is the request flow?
1. **Application Launch**: The user runs the Streamlit app (`streamlit run streamlit_app.py`).
2. **LLM Initialization**: The HuggingFace text-generation pipeline (`SmolLM2-360M-Instruct`) is loaded and cached in Streamlit session state.
3. **Document Upload**: The user uploads a PDF, DOCX, or TXT file through the UI file uploader.
4. **Text Extraction**:
   - `src/loader.py` checks the extension.
   - Text is extracted using `pypdf` (PDF), `docx2txt` (Word), or direct read (TXT).
5. **Text Chunking**: The raw text is split into overlapping chunks (size=300 characters, overlap=50) using LangChain's `RecursiveCharacterTextSplitter`.
6. **Vectorization & Indexing**: The chunks are converted into float vectors using HuggingFace BGE embeddings (`bge-small-en-v1.5`) and stored in a FAISS index.
7. **User Query**:
   - The user inputs a question in the chat bar.
   - FAISS performs similarity search (`k=1`) to retrieve the top matching chunk context.
   - A prompt is assembled with the context and user question.
   - The SmolLM2 LLM generates the final answer text based strictly on the retrieved context snippet.
   - The response is rendered on the Streamlit chat UI.

## 3. Which packages are used and why?
- **`streamlit`**: Implements the SaaS-like web layout, chat interface, file uploading widgets, and session states.
- **`langchain-huggingface`**: Integrates HuggingFace models for local sentence embedding calculations.
- **`langchain-community` & `faiss-cpu`**: Handles local vector storage, indexing, and similarity searches.
- **`pypdf` & `docx2txt`**: Used for reading and parsing text content from uploaded PDF and Word documents.
- **`transformers`**: HuggingFace library used to run the local instruction-following text-generation model pipeline (`SmolLM2-360M-Instruct`).

## 4. Where does the data come from?
The data comes from user-uploaded documents (PDF, DOCX, TXT) and queries typed into the chat interface.

## 5. Where is the data stored?
- Uploaded files are temporarily written using `tempfile.NamedTemporaryFile`.
- Computed vector coordinates and FAISS index are stored dynamically in RAM inside the Streamlit session state variable (`st.session_state.vectorstore`). No persistent database is created on disk.

## 6. What is the role of the LLM?
The local LLM (`HuggingFaceTB/SmolLM2-360M-Instruct`) processes the user prompt, reads the retrieved document context, and formulates a concise, conversational answer strictly based on the context.

## 7. What breaks if the LLM is removed?
If the LLM is removed, the generative answer formulation will fail. The system will still be able to retrieve the most similar raw document chunks from the vector store but will not be able to synthesize conversational replies.
