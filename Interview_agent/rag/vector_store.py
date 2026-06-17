from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

chunks = []
index = None

def create_index(text):

    global chunks
    global index

    chunks = text

    embeddings = model.encode(text)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings).astype("float32")
    )


    def search(query, k=3):

    embedding = model.encode([query])

    distances, ids = index.search(
        np.array(embedding).astype("float32"),
        k
    )

    return [chunks[i] for i in ids[0]]