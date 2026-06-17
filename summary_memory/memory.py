class SummaryMemory:

    def __init__(
        self,
        file_name="summary_memory.txt"
    ):
        self.file_name = file_name

    def save(self, content):

        with open(
            self.file_name,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(content)
            file.write("\n\n")