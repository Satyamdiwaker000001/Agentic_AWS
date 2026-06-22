# Buffer Memory - Documentation

## 1. What does the project do?
This project is a simple conversation logging system. It stores user messages and agent responses in a local text file to maintain conversation logs.

## 2. What is the request flow?
1. **Initialization**: The user runs `main.py`. The script instantiates `BufferMemory`, which creates `chat_memory.txt` if it does not already exist.
2. **Interactive Loop**:
   - `exit`: Quits the program.
   - `memory`: Reads the entire content of `chat_memory.txt` and prints it to the console.
   - `clear`: Overwrites `chat_memory.txt` with an empty string.
   - Normal text input:
     - Appends `User: <input>` to `chat_memory.txt` using `save_message`.
     - Generates a dummy agent response ("I received your message: ...").
     - Appends `Agent: <response>` to `chat_memory.txt`.
     - Prints the agent response to the console.

## 3. Which packages are used and why?
- **`os` (standard library)**: Used to verify file paths and check if the memory file exists.

## 4. Where does the data come from?
The data comes from user keyboard inputs entered in the terminal console at runtime.

## 5. Where is the data stored?
The conversation logs are stored in a local flat text file: `chat_memory.txt`.

## 6. What is the role of the LLM?
There is **no LLM model used** in this project. The agent's response is a static string template constructed using python string interpolation.

## 7. What breaks if the LLM is removed?
**Nothing breaks**, since the project is fully independent of any LLM or AI models.
