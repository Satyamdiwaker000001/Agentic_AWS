from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import gradio as gr

# ----------------------------
# Read Resume PDF
# ----------------------------

def load_resume(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


resume_text = load_resume("resume.pdf")

# ----------------------------
# Split Text into Chunks
# ----------------------------

def chunk_text(text, chunk_size=500):
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]


chunks = chunk_text(resume_text)

# ----------------------------
# Embedding Model (~90MB)
# ----------------------------

print("Loading embeddings...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

embeddings = embedding_model.encode(
    chunks,
    convert_to_numpy=True
)

# ----------------------------
# FAISS Index
# ----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ----------------------------
# Search
# ----------------------------

def ask_resume(question):

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        3
    )

    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return "\n\n".join(results)

# ----------------------------
# UI
# ----------------------------

demo = gr.Interface(
    fn=ask_resume,
    inputs=gr.Textbox(
        lines=2,
        placeholder="Ask about the resume..."
    ),
    outputs=gr.Textbox(lines=10),
    title="Resume Chatbot"
)

demo.launch()