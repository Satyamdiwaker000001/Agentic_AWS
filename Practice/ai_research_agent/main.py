import os
from dotenv import load_dotenv
from agent.core import ReActResearchAgent

# Load local environment settings
load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("CRITICAL ERROR: Please configure OPENAI_API_KEY inside your .env file.")
        return

    agent = ReActResearchAgent()
    
    print("==============================================")
    # Corrected simple unit display
    print("  Autonomous ReAct Research Agent Initialized  ")
    print("==============================================")
    
    query = input("\nWhat research topic would you like to explore today?\n> ")
    if query.strip():
        report = agent.execute(query)
        print("\n==============================================")
        print("                FINAL REPORT                  ")
        print("==============================================")
        print(report)

if __name__ == "__main__":
    main()