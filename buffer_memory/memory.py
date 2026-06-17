import os

class BufferMemory:

    def __init__(self, memory_file="chat_memory.txt"):
        self.memory_file = memory_file

        if not os.path.exists(self.memory_file):
            open(self.memory_file, "w", encoding="utf-8").close()

    def save_message(self, role, message):

        with open(self.memory_file, "a", encoding="utf-8") as file:
            file.write(f"{role}: {message}\n")

    def get_memory(self):

        with open(self.memory_file, "r", encoding="utf-8") as file:
            return file.read()

    def clear_memory(self):

        with open(self.memory_file, "w", encoding="utf-8") as file:
            file.write("")