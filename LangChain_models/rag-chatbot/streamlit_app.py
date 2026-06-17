import tempfile

try:
    import streamlit as st  # type: ignore[import]
except ImportError as exc:
    raise ImportError(
        "streamlit is required to run this app. Install it with `pip install streamlit`."
    ) from exc

from src.loader import load_document
from src.splitter import create_chunks
from src.vectorstore import create_vector_store
from src.llm import get_llm
from src.rag_chain import ask_rag

st.set_page_config(
    page_title="RAG Chatbot",
    layout="wide"
)

st.title("📄 RAG Chatbot")
st.write("Upload a document and start chatting.")

# Load LLM only once
if "llm" not in st.session_state:

    with st.spinner("Loading LLM..."):

        st.session_state.llm = get_llm()

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "txt", "docx"]
)

if uploaded_file:

    if "current_file" not in st.session_state or \
       st.session_state.current_file != uploaded_file.name:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{uploaded_file.name.split('.')[-1]}"
        ) as tmp:

            tmp.write(uploaded_file.read())

            temp_path = tmp.name

        with st.spinner("Processing document..."):

            text = load_document(temp_path)

            chunks = create_chunks(text)

            st.session_state.vectorstore = (
                create_vector_store(chunks)
            )

            st.session_state.current_file = (
                uploaded_file.name
            )

        st.success(
            f"{uploaded_file.name} loaded successfully"
        )

    question = st.chat_input(
        "Ask a question..."
    )

    if question:

        with st.chat_message("user"):

            st.write(question)

        with st.spinner("Thinking..."):

            answer = ask_rag(
                question,
                st.session_state.vectorstore,
                st.session_state.llm
            )

        with st.chat_message("assistant"):

            st.write(answer)