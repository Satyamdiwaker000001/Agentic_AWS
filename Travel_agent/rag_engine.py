# ============================================================
# IMPORTS
# ============================================================

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# CONFIG
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

VECTOR_DB_PATH = "./vectorstore"


# ============================================================
# FEATURE 04 : DOCUMENT CREATION
# ============================================================

def create_documents(df):
    """
    Convert dataset rows into LangChain Documents.
    """

    documents = []

    for _, row in df.iterrows():

        content = f"""
Destination: {row.get('Destination', 'Unknown')}

Duration: {row.get('Duration (days)', 0)} days

Traveler Gender: {row.get('Traveler gender', 'Unknown')}

Traveler Nationality: {row.get('Traveler nationality', 'Unknown')}

Accommodation Type: {row.get('Accommodation type', 'Unknown')}

Accommodation Cost: {row.get('Accommodation cost', 0)}

Transportation Type: {row.get('Transportation type', 'Unknown')}

Transportation Cost: {row.get('Transportation cost', 0)}
"""

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "destination": row.get("Destination", "Unknown")
                }
            )
        )

    print(f"[SUCCESS] Created {len(documents)} Documents")

    return documents


# ============================================================
# FEATURE 05 : EMBEDDING GENERATION
# ============================================================

def load_embedding_model():
    """
    Load HuggingFace embedding model.
    """

    print("[INFO] Loading Embedding Model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("[SUCCESS] Embedding Model Loaded")

    return embeddings


# ============================================================
# FEATURE 06 : CHROMADB RETRIEVAL
# ============================================================

def build_vectorstore(documents):
    """
    Create Chroma Vector Database.
    """

    embeddings = load_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    print("[SUCCESS] ChromaDB Created")

    return vectorstore


def load_vectorstore():
    """
    Load Existing ChromaDB.
    """

    embeddings = load_embedding_model()

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vectorstore


def retrieve_documents(query, k=5):
    """
    Retrieve similar documents.
    """

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        query=query,
        k=k
    )

    return results


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    from data_engine import (
        load_dataset,
        validate_dataset,
        clean_dataset
    )

    FILE_PATH = "Travel_agent/Travel details dataset.csv"

    df = load_dataset(FILE_PATH)

    if df is not None:

        if validate_dataset(df):

            df = clean_dataset(df)

            docs = create_documents(df)

            build_vectorstore(docs)

            results = retrieve_documents(
                "cheap destinations"
            )

            print("\nRETRIEVED DOCUMENTS\n")

            for doc in results:

                print(doc.page_content)

                print("-" * 50)