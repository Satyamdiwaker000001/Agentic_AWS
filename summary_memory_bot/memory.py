class SummaryMemory:

    def __init__(self, memory_file="summary_memory.txt"):
        self.memory_file = memory_file

    def save_summary(self, summary):

        with open(self.memory_file, "w", encoding="utf-8") as file:
            file.write(summary)

    def load_summary(self):

        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                return file.read()

        except FileNotFoundError:
            return ""

    def clear(self):

        with open(self.memory_file, "w", encoding="utf-8") as file:
            file.write("")