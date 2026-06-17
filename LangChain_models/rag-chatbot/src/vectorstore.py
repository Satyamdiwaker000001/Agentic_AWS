from langchain_community.vectorstores import FAISS

from src.embeddings import (
    get_embedding_model
)


def create_vector_store(chunks):

    embeddings = get_embedding_model()

    return FAISS.from_texts(
        chunks,
        embeddings
    )