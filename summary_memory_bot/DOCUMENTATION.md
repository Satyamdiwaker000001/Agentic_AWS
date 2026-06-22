# Summary Memory Bot - Documentation

## 1. What does the project do?
This project is an offline rule-based conversation summary memory bot. It processes user chat messages to extract specific information (such as user name, learning topics, and interests), updates a running summary, and stores it in a local text file.

## 2. What is the request flow?
1. **App Launch**: The user runs `main.py` which instantiates `SummaryMemory`.
2. **Current Summary Load**: The script loads the existing summary from `summary_memory.txt`.
3. **Interactive Loop**:
   - `exit`: Quits the program.
   - `memory`: Prints the current summary memory context to the console.
   - User inputs a message:
     - The message is analyzed by `update_summary()`.
     - Substring checks look for key phrases:
       - `"my name is"` -> extracts name and appends `User name: {name}`.
       - `"i am learning"` -> extracts topic and appends `Learning: {topic}`.
       - `"i like"` -> extracts interest and appends `Interest: {interest}`.
       - If no key phrases match, the summary remains unchanged.
     - The updated summary is written back to `summary_memory.txt`.
     - The bot prints a confirmation response: `"Bot: I have updated my summary memory."`

## 3. Which packages are used and why?
There are **no third-party packages used** in this project. It is implemented entirely using Python's standard built-in functions.

## 4. Where does the data come from?
The data comes from user keyboard inputs entered in the terminal console at runtime.

## 5. Where is the data stored?
The summarized information is stored in a local flat text file: `summary_memory.txt`.

## 6. What is the role of the LLM?
There is **no LLM model used** in this project. The system relies entirely on static string partitioning and conditional statement checks.

## 7. What breaks if the LLM is removed?
**Nothing breaks**, since the project has no AI model dependencies.
