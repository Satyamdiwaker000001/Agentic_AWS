class SummaryMemory:

    def __init__(self, file_name="summary_memory.txt"):
        self.file_name = file_name

    def save(self, content):

        with open(
            self.file_name,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

    def load(self):

        try:
            with open(
                self.file_name,
                "r",
                encoding="utf-8"
            ) as file:

                return file.read()

        except FileNotFoundError:
            return ""