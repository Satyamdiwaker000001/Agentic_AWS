# AI Research Agent - Documentation

## 1. What does the project do?
This project is an autonomous AI Research Agent implementing the ReAct (Reasoning and Acting) framework. It takes user research queries, executes an iterative thought-action loop, triggers local/web tools to gather information, and compiles comprehensive reports.

## 2. What is the request flow?
1. **Startup**: The user runs `main.py` which loads environment variables (`OPENAI_API_KEY`) from local `.env`.
2. **User Input**: The agent prompts the user to enter a research topic and runs `agent.execute()`.
3. **ReAct Execution Loop**: Loops start (max loops = 5):
   - The agent sends the conversation history to the OpenAI completions endpoint (configured to run `gemini-2.5-flash`).
   - The model generates its cognitive thoughts and plans the next step.
   - The response is analyzed:
     - If it contains `"FINAL ANSWER:"`, the loop terminates and the final report is displayed.
     - If it contains a tool trigger pattern, the corresponding tool function is executed:
       - `web_search(query)`: Sends a GET request to the DuckDuckGo JSON API to fetch abstract details.
       - `text_summarizer(text)`: Concatenates the first 5 lines of the text.
     - The output is formatted as `OBSERVATION: <output>` and saved back into conversation history memory.
     - The loop re-enters for the next turn.

## 3. Which packages are used and why?
- **`openai`**: SDK to connect to the completions API to run the core agent model (`gemini-2.5-flash`).
- **`requests`**: Performs HTTP GET requests to fetch search query results from DuckDuckGo API.
- **`python-dotenv`**: Loads API keys and configurations from the local `.env` file.

## 4. Where does the data come from?
- Research queries: User input.
- Research results: DuckDuckGo public search JSON responses.

## 5. Where is the data stored?
All conversation logs and memory updates are stored in RAM within the `ConversationMemory` array. No persistent logs are saved to disk.

## 6. What is the role of the LLM?
The LLM (`gemini-2.5-flash`) acts as the central brain. It evaluates query contexts, coordinates tool execution, parses observation responses, and compiles final research reports.

## 7. What breaks if the LLM is removed?
The autonomous research loop will break entirely. The system will not be able to choose tools dynamically, extract search terms, or compile findings.
