# Agentic AWS - AI Projects Showcase

A comprehensive collection of AI agents, LLM applications, and machine learning projects built with Python, exploring various aspects of agentic AI, RAG systems, and automation.

---

## 📋 Projects Overview & Models Used

Below is a detailed overview of every project included in this repository. Click on any project name to navigate directly to its directory.

### 1. [Attendance Agent](./Attendece_agent/)

**Purpose:** Automated attendance analysis and fine calculation system  
**Models & Technologies:**
- **Core Stack**: Pandas, Scikit-learn
- **Data Source**: Direct analysis of CSV attendance records
- **Why These Models**: Lightweight, no LLM needed for rule-based analysis. Fast computation for generating reports on fine calculations based on employee attendance patterns (safe/danger zones).

---

### 2. [Day-5 / Embedding](./Day-5/Embedding/)

**Purpose:** Memory management system with semantic embeddings and retrieval  
**Models & Technologies:**
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Framework**: Sentence Transformers
- **Why This Model**: Lightweight (22MB), fast inference on CPU, excellent for semantic similarity and privacy-preserving offline retrieval.

---

### 3. [Interview Agent](./Interview_agent/)

**Purpose:** AI-powered interview system with speech processing and document analysis  
**Models & Technologies:**
- **Model**: `llama_cpp` (Local LLaMA inference)
- **RAG Stack**: FAISS, pypdf, Text-to-Speech (TTS), and Speech-to-Text (STT)
- **Why This Architecture**: RAG enables context-aware responses directly from candidate resumes. Speech processing creates a natural conversational interface, and local LLaMA ensures private, responsive interactions.

---

### 4. [LangChain RAG Chatbot](./LangChain_models/rag-chatbot/)

**Purpose:** Document-based question-answering system using Retrieval-Augmented Generation  
**Models & Technologies:**
- **Embedding Model**: `BAAI/bge-small-en-v1.5` (via HuggingFaceEmbeddings)
- **LLM**: `HuggingFaceTB/SmolLM2-360M-Instruct`
- **Vector Store**: FAISS
- **Why This Architecture**: BGE embeddings offer state-of-the-art semantic search. SmolLM2 provides a lightweight but capable instruction-following engine. The LangChain integration abstracts the complex RAG pipeline effectively.

---

### 5. [Resume Analyzer](./Resume_Analyser/)

**Purpose:** Match resumes against job descriptions using semantic similarity  
**Models & Technologies:**
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Similarity Metric**: Cosine similarity scoring
- **Why This Model**: Perfect for offline analysis; sentence-level embeddings accurately capture resume semantics to generate interpretable matching scores.

---

### 6. [ResumePilot AI](./ResumePilot_AI/)

**Purpose:** Full-stack resume analysis platform with ATS optimization  
**Models & Technologies:**
- **LLM Integration Options**: OpenAI, Claude, AWS Bedrock
- **Backend Stack**: FastAPI, SQLite
- **Frontend Stack**: React, Vite, Tailwind CSS, Framer Motion
- **Why This Stack**: High-performance asynchronous backend with an interactive, beautifully animated React frontend. Designed for real-time analysis feedback, ATS score calculations, and skill gap analysis.

---

### 7. [Travel Agent](./Travel_agent/)

**Purpose:** RAG-based AI travel assistant for intelligent destination recommendations  
**Models & Technologies:**
- **LLM**: `HuggingFaceTB/SmolLM2-1.7B-Instruct`
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Why This Architecture**: The 1.7B SmolLM2 provides solid reasoning for travel planning, while MiniLM embeddings allow efficient document/knowledge retrieval to ground the agent's recommendations in factual travel data.

---

### 8. [Buffer Memory](./buffer_memory/)

**Purpose:** Simple conversation memory system  
**Models & Technologies:**
- **Core**: Python classes for memory management and text file persistence
- **Why This Approach**: A lightweight, non-LLM dependent system perfect for simple chatbots that need to retain conversation history.

---

### 9. [PDF Summary](./pdf_summary/)

**Purpose:** Automatic summarization of PDF documents  
**Models & Technologies:**
- **Model**: Hugging Face Transformers pipelines (Summarization)
- **Processing**: pypdf extraction, persistent memory
- **Why This Architecture**: Capable of chunking long documents and generating concise summaries that are stored for later reference.

---

### 10. [Resume Chatbot](./resume_chatbot/)

**Purpose:** Interactive chatbot trained on resume data  
**Models & Technologies:**
- **Core**: RAG concepts applied to resume parsing and conversation management
- **Why This Architecture**: Allows recruiters or users to interactively extract specific details (e.g., experience, skills) from a resume via chat.

---

### 11. [Summary Memory](./summary_memory/)

**Purpose:** Advanced document summarization with persistent memory  
**Models & Technologies:**
- **Model**: `facebook/bart-large-cnn`
- **Why This Model**: BART Large CNN is explicitly trained on summarization, offering high-quality abstractive summaries rather than just extractive extraction. It handles various document lengths excellently.

---

### 12. [Summary Memory Bot](./summary_memory_bot/)

**Purpose:** Conversational interface for document summarization  
**Models & Technologies:**
- **Core**: Memory management intertwined with summarization pipelines
- **Why This Architecture**: Provides a seamless chat-based interface to interactively summarize large contexts over time.

---

### 13. [Window Memory](./window_memory/)

**Purpose:** Sliding window memory management for conversations  
**Models & Technologies:**
- **Core**: Window-based message storage algorithms
- **Why Window Memory**: Maintains recent context without overloading the LLM's token limit, offering a low computational cost solution for long conversations.

---

### 14. [AI Research Agent (Practice)](./Practice/ai_research_agent/)

**Purpose:** Autonomous ReAct (Reasoning + Acting) agent for research tasks  
**Models & Technologies:**
- **Model**: `gemini-2.5-flash`
- **Pattern**: ReAct framework
- **Why ReAct**: Combines reasoning with tool usage (like web search) for complex multi-step tasks. Gemini 2.5 Flash offers fast and reliable tool-calling capabilities.

---

### 15. [Text to Speech (Practice)](./Practice/Text_to_speech/)

**Purpose:** Text-to-speech synthesis system  
**Models & Technologies:**
- **Engine**: gTTS (Google Text-to-Speech)
- **Why This Engine**: Easy integration for converting text to natural speech across multiple languages.

---

### 16. [Voice Calculator](./Voice_Calculator/)

**Purpose:** AI-powered voice command calculator  
**Models & Technologies:**
- **LLM**: `Qwen/Qwen2.5-0.5B-Instruct`
- **Audio Processing**: SpeechRecognition, pyttsx3
- **Why This Architecture**: A local, fast LLM handles complex and messy voice command inputs reliably, replacing brittle string-matching logic for evaluating mathematical intent natively on CPU/GPU.

---

### 17. [SmartChunk AI](./smartchunk-ai/)

**Purpose:** Intelligent Document Parsing & Chunking Engine  
**Models & Technologies:**
- **Model**: `sentence-transformers/all-MiniLM-L6-v2` (for Semantic Chunking)
- **Frameworks**: FastAPI (Backend), Vite + React (Frontend)
- **Why This Architecture**: Provides fixed-size, recursive, and semantic text chunking algorithms crucial for robust Retrieval-Augmented Generation (RAG) pipelines, with a modern, glassmorphism UI for testing.

---

## 🏗️ Architecture Patterns & Insights

### RAG (Retrieval-Augmented Generation)
Used heavily in projects like **RAG Chatbot**, **Interview Agent**, **Resume Analyzer**, and **Travel Agent**.
`Document → Chunk → Embed → Store → Query → Retrieve → LLM → Answer`

### Memory Systems Comparison
- **Buffer Memory**: Retains the entire conversation history. Simple but does not scale well with tokens.
- **Window Memory**: Retains a sliding context window. Highly efficient.
- **Summary Memory**: Condenses long-term memory via summarization models (`BART-large-cnn`), allowing abstraction over long dialogues.

### Selected Model Matrix

| Model | Type | Used In | Characteristics |
| :--- | :--- | :--- | :--- |
| **`all-MiniLM-L6-v2`** | Embeddings | Day-5, Resume Analyzer, Travel Agent, SmartChunk AI | Lightweight (22MB), fast CPU inference, good for general similarity. |
| **`bge-small-en-v1.5`** | Embeddings | LangChain RAG Chatbot | Maximum accuracy for document retrieval. |
| **`SmolLM2-360M`** | LLM | LangChain RAG Chatbot | Ultra-lightweight instruction-following. |
| **`SmolLM2-1.7B`** | LLM | Travel Agent | Stronger reasoning capabilities while remaining local. |
| **`gemini-2.5-flash`** | LLM | AI Research Agent | Excellent tool-calling and reasoning for ReAct patterns. |
| **`bart-large-cnn`** | LLM (Seq2Seq) | Summary Memory | High-quality abstractive document summarization. |
| **`llama_cpp`** | LLM | Interview Agent | Local, privacy-first conversational capabilities. |
| **`Qwen2.5-0.5B`** | LLM | Voice Calculator | High-speed math parsing from transcribed voice logic. |
| **GPT-4 / Claude / Bedrock** | LLM APIs | ResumePilot AI | Complex reasoning and production-grade deployments. |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for React frontends)
- Virtual environment (`venv`)

### Installation

```bash
# Clone repository
git clone https://github.com/Satyamdiwaker000001/Agentic_AWS.git
cd Agentic_AWS

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Projects

**Travel Agent (RAG):**
```bash
cd Travel_agent
python ai_engine.py
```

**Resume Analyzer:**
```bash
cd Resume_Analyser
python main.py
```

**RAG Chatbot (Streamlit):**
```bash
cd LangChain_models/rag-chatbot
streamlit run streamlit_app.py
```

**ResumePilot AI (Full-Stack):**
```bash
# Terminal 1 - Backend
cd ResumePilot_AI/Backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd ResumePilot_AI/Frontend
npm install
npm run dev
```

**SmartChunk AI (Full-Stack):**
```bash
# Terminal 1 - Backend
cd smartchunk-ai
python -m uvicorn app:app --reload

# Terminal 2 - Frontend
cd smartchunk-ai/frontend
npm install
npm run dev
```

---

## 🔮 Future Enhancements

1. **Integration with Production LLMs**: Migrate more proofs-of-concept to robust APIs like Claude, GPT-4, and AWS Bedrock.
2. **Multi-Language Support**: Expand the Text-to-Speech and prompt architectures to support a global audience.
3. **Advanced Memory Management**: Implement semantic deduplication in vector stores.
4. **Agent Swarms**: Enable individual agents (e.g., Interview Agent + Resume Analyzer) to communicate with one another.
5. **Deployment**: Automate deployment of FastAPI and Streamlit apps to AWS services like Lambda and SageMaker.

---

## 📄 License & Author

**Author**: [Satyam Diwaker](https://github.com/Satyamdiwaker000001)  
**License**: MIT License  
**Status**: Active Development (Updated June 2026)  

Contributions, issues, and feature requests are welcome!
