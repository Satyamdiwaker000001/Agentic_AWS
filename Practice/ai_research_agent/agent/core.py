import os
from openai import OpenAI
from .memory import ConversationMemory
from .tools import AVAILABLE_TOOLS

class ReActResearchAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
        self.model = os.getenv("MODEL_NAME", "gemini-2.5-flash")
        self.memory = ConversationMemory()
        self.max_loops = 5
        
        # System prompt ko thoda strict banaya hai taaki Gemini JSON use na kare
        self.system_prompt = (
            "You are an expert AI Research Agent.\n"
            "You MUST strictly follow this exact format for actions.\n"
            "To search the web, output exactly: ACTION: web_search(your_search_term)\n"
            "To summarize, output exactly: ACTION: text_summarizer(your_text)\n"
            "DO NOT use JSON formatting for actions.\n"
            "When you have enough information, output exactly: FINAL ANSWER: followed by your detailed report."
        )

    def _get_tools_description(self) -> str:
        desc = ""
        for name, config in AVAILABLE_TOOLS.items():
            desc += f"- {name}: {config['description']}\n"
        return desc

    def execute(self, user_query: str) -> str:
        self.memory.clear()
        self.memory.add_message("system", self.system_prompt)
        self.memory.add_message("user", user_query)
        
        print(f"\n[Agent Startup] Initiating research on: '{user_query}'")
        
        for loop_count in range(self.max_loops):
            print(f"\n--- Loop Turn {loop_count + 1} ---")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.memory.get_messages(),
                temperature=0.2
            )
            
            response_text = response.choices[0].message.content
            print(f"[Thought/Response]:\n{response_text}")
            self.memory.add_message("assistant", response_text)
            
            # Case-insensitive check for final answer
            if "final answer:" in response_text.lower() or "final report" in response_text.lower():
                return response_text
                
            action_triggered = False
            for tool_name in AVAILABLE_TOOLS:
                if tool_name in response_text:
                    arg = user_query 
                    # Extract argument carefully
                    if "(" in response_text and ")" in response_text:
                        try:
                            # Split based on tool name to get the parameter
                            arg = response_text.split(tool_name + "(")[1].split(")")[0].strip("'\"")
                        except Exception:
                            pass
                    
                    # Execute tool
                    observation = AVAILABLE_TOOLS[tool_name]["function"](arg)
                    print(f"\n[Observation]:\n{observation}")
                    
                    self.memory.add_message("user", f"OBSERVATION: {observation}")
                    action_triggered = True
                    break
            
            if not action_triggered:
                print("[Notice] No definitive action recognized. Continuing cycle...")
                self.memory.add_message("user", "Please continue analyzing or provide the FINAL ANSWER:")
                
        return "Research loop timed out before finalizing a comprehensive report."