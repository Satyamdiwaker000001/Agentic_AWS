# AI Research Agent (ReAct Framework)

An autonomous AI Research Agent built from scratch in Python utilizing the ReAct framework and OpenAI-compatible tool-calling.

## Setup Instructions

1. **Clone or create the project directory** and navigate into it.
2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   Install dependencies:

Bash
pip install -r requirements.txt
Set up environment variables:

Bash
cp .env.example .env
Open .env and fill in your OPENAI_API_KEY.

Running the Agent
Execute the main script to start the interactive research session:

Bash
python main.py

---

## 3. Core Implementation Source Code

### `agent/memory.py`
Manages the short-term conversation context so the agent remembers previous steps and interactions.

```python
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
        self.history =