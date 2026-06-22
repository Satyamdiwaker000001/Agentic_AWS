# Window Memory - Documentation

## 1. What does the project do?
This project implements a sliding window conversation memory system. It retains only the most recent conversation exchange lines (default window size = 6 messages, which is 3 user-agent interactions). When new messages are added and the window size is exceeded, the oldest messages are automatically discarded to maintain token efficiency.

## 2. What is the request flow?
1. **Startup**: The user runs `main.py` which instantiates `WindowMemory` with a deque of max size 6.
2. **Interactive Loop**:
   - `exit`: Quits the program.
   - `memory`: Prints the current active messages inside the sliding window deque.
   - User inputs a message:
     - The message is appended to the window deque as `User: {message}`.
     - If the total messages in the deque exceed 6, the oldest line is automatically evicted.
     - The current deque lines are joined and written to `window_memory.txt`.
     - The bot generates a response ("I received: {user_message}").
     - The response is appended to the deque as `Bot: {response}`, and the file is overwritten again.

## 3. Which packages are used and why?
There are **no third-party packages used** in this project. It uses standard python collections (`collections.deque`) to implement the sliding queue structure.

## 4. Where does the data come from?
The data comes from user keyboard inputs entered in the terminal console at runtime.

## 5. Where is the data stored?
The current active sliding window context is saved to a local flat text file: `window_memory.txt`.

## 6. What is the role of the LLM?
There is **no LLM model used** in this project. The bot response is a static string template constructed using python string formatting.

## 7. What breaks if the LLM is removed?
**Nothing breaks**, since the project is fully independent of any AI models.
