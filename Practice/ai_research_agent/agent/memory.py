class ConversationMemory:
    """Manages the conversation history and inner thoughts of the agent."""
    def __init__(self):
        self.history = []

    def add_message(self, role: str, content: str):
        """Adds a message to the conversation log."""
        self.history.append({"role": role, "content": content})

    def get_messages(self):
        """Retrieves all stored logs for the LLM context."""
        return self.history

    def clear(self):
        """Resets the memory state."""
        self.history = []