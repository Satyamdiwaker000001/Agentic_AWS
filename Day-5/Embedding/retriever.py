import pickle
import os

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from config import VECTOR_FILE

from embedding_model import (
    EmbeddingModel
)

from memory_manager import (
    MemoryManager
)


class Retriever:

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.memory = MemoryManager()

        os.makedirs(
            "embeddings",
            exist_ok=True
        )

    def build_embeddings(self):

        memories = self.memory.get_memories()

        vectors = []

        for text in memories:

            vectors.append(
                self.embedder.encode(text)
            )

        with open(
            VECTOR_FILE,
            "wb"
        ) as file:

            pickle.dump(
                vectors,
                file
            )

    def search(self, query):

        memories = self.memory.get_memories()

        with open(
            VECTOR_FILE,
            "rb"
        ) as file:

            vectors = pickle.load(file)

        query_vector = (
            self.embedder.encode(query)
        )

        scores = cosine_similarity(
            [query_vector],
            vectors
        )[0]

        best_index = scores.argmax()

        return memories[best_index]