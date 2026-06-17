import os
import sys

print("""
=========================================
RAG CHATBOT
=========================================

Available Modes:

1. GUI Mode
   streamlit run streamlit_app.py

2. CLI Mode
   python cli_chatbot.py

=========================================
""")

if __name__ == "__main__":

    os.system(
        "streamlit run streamlit_app.py"
    )

