import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from utils import load_data


# -----------------------------
# File Paths
# -----------------------------
ERROR_FILE = "data/errors.txt"
SOLUTION_FILE = "data/solutions.txt"

VECTOR_DB_PATH = "vector_db"


def build_vector_database():
    print("Loading data...")

    documents = load_data(ERROR_FILE, SOLUTION_FILE)

    print(f"Loaded {len(documents)} error records.")

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating FAISS index...")

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    os.makedirs(VECTOR_DB_PATH, exist_ok=True)

    vector_store.save_local(VECTOR_DB_PATH)

    print("\nVector Database created successfully!")
    print(f"Saved at: {VECTOR_DB_PATH}")


if __name__ == "__main__":
    build_vector_database()