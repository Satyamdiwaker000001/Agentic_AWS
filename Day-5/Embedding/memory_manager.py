import os

from config import MEMORY_FILE


class MemoryManager:

    def __init__(self):

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(MEMORY_FILE):

            with open(
                MEMORY_FILE,
                "w",
                encoding="utf-8"
            ):
                pass

    def add_memory(self, text):

        with open(
            MEMORY_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(text + "\n")

    def get_memories(self):

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return [
                line.strip()
                for line in file.readlines()
                if line.strip()
            ]