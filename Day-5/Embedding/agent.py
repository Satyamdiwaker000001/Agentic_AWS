from memory_manager import (
    MemoryManager
)

from retriever import Retriever


class Agent:

    def __init__(self):

        self.memory = MemoryManager()

        self.retriever = Retriever()

    def save(self, text):

        self.memory.add_memory(text)

        self.retriever.build_embeddings()

    def recall(self, query):

        return self.retriever.search(
            query
        )