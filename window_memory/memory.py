from collections import deque
from Agentic.window_memory.config import WINDOW_SIZE, MEMORY_FILE


class WindowMemory:

    def __init__(self):

        self.window = deque(
            maxlen=WINDOW_SIZE
        )

        self.memory_file = MEMORY_FILE

    def add_message(
        self,
        role,
        message
    ):

        self.window.append(
            f"{role}: {message}"
        )

        self.save()

    def get_context(self):

        return "\n".join(
            self.window
        )

    def save(self):

        with open(
            self.memory_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                self.get_context()
            )

    def clear(self):

        self.window.clear()

        with open(
            self.memory_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("")