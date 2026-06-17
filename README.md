# Agentic AWS - AI Projects Showcase

A comprehensive collection of AI agents, LLM applications, and machine learning projects built with Python, exploring various aspects of agentic AI, RAG systems, and automation.

---

## 📋 Projects Overview & Models Used

### 1. **Attendance Agent** (`Attendece_agent/`)

**Purpose:** Automated attendance analysis and fine calculation system  
**Models & Technologies:**

- **Pandas**: Data manipulation and CSV processing
- **Scikit-learn**: Data analysis and statistical computations
- **CSV Processing**: Direct analysis of attendance records

**Why These Models:**

- Lightweight, no LLM needed for rule-based attendance analysis
- Efficient for tabular data processing
- Fast computation for generating reports on fine calculations

**Key Features:**

- Parses attendance records (2023-2024)
- Calculates fines for employees
- Generates reports for safe and danger employees

---

### 2. **Day-5/Embedding** (`Day-5/Embedding/`)

**Purpose:** Memory management system with semantic embeddings and retrieval  
**Models & Technologies:**

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Framework**: Sentence Transformers
- **Storage**: Pickle-based vector storage

**Why This Model:**

- Lightweight (22MB) - fast inference on CPU
- Excellent for semantic similarity and memory retrieval
- Good balance between speed and accuracy
- Open-source and privacy-preserving

**Key Features:**

- Encodes user queries and memories as vectors
- Retrieves relevant memories based on semantic similarity
- Persistent vector storage system

---

### 3. **Interview Agent** (`Interview_agent/`)

**Purpose:** AI-powered interview system with speech processing and document analysis  
**Models & Technologies:**

- **RAG Components**: Vector embeddings, PDF parsing, semantic search
- **Speech**: Text-to-Speech (TTS) and Speech-to-Text (STT)
- **Vector Store**: FAISS for efficient similarity search
- **PDF Processing**: pypdf for resume parsing

**Why This Architecture:**

- RAG enables context-aware responses from resume documents
- Speech processing creates natural human-computer interaction
- FAISS provides fast semantic search through resume content

**Key Features:**

- Resume-based RAG system
- Real-time speech interaction
- Document embedding and retrieval

---

### 4. **LangChain RAG Chatbot** (`LangChain_models/rag-chatbot/`)

**Purpose:** Document-based question-answering system using Retrieval-Augmented Generation  
**Models & Technologies:**

**Embeddings**:

- Model: `BAAI/bge-small-en-v1.5` (via HuggingFaceEmbeddings)
- Library: LangChain + HuggingFace

**LLM**:

- Model: `HuggingFaceTB/SmolLM2-360M-Instruct`
- Framework: Transformers pipeline
- Context: 100 token generation, 0.1 temperature

**Vector Store**:

- FAISS for efficient similarity search
- Langchain integration

**Text Processing**:

- RecursiveCharacterTextSplitter (chunk_size=300, overlap=50)
- Support for PDF, DOCX, TXT files

**Why This Architecture:**

- `BGE embeddings`: State-of-the-art performance on semantic search
- `SmolLM2`: Lightweight but capable instruction-following model
- FAISS: Scales to millions of documents with fast retrieval
- LangChain: Abstracts complexity of RAG pipeline

**Key Features:**

- Upload documents (PDF/DOCX/TXT)
- Ask questions about document content
- Streaming responses
- Streamlit web interface

---

### 5. **Resume Analyzer** (`Resume_Analyser/`)

**Purpose:** Match resumes against job descriptions using semantic similarity  
**Models & Technologies:**

- **Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Similarity**: Cosine similarity scoring
- **PDF Processing**: pypdf

**Why This Model:**

- Lightweight embedding model perfect for offline analysis
- Sentence-level embeddings capture resume semantics
- Cosine similarity provides interpretable matching scores

**Key Features:**

- Parse multiple resumes (PDF)
- Compare against job description
- Generate similarity scores
- Rank resumes by match percentage

---

### 6. **ResumePilot AI** (`ResumePilot_AI/`)

**Purpose:** Full-stack resume analysis platform with ATS optimization

#### Backend (`Backend/`)

**Technologies:**

- **Framework**: FastAPI
- **Analysis**: Mock AI scoring (ready for LLM integration with Claude/GPT)
- **File Processing**: PDF/DOCX parsing
- **Database**: SQLite (view_db.py)

**Why FastAPI:**

- High performance async framework
- Auto-generated API documentation
- Type-safe with Pydantic validation
- Easy to integrate LLMs (OpenAI, Anthropic, Bedrock)

#### Frontend (`Frontend/`)

**Technologies:**

- **Framework**: React + Vite
- **UI Library**: Tailwind CSS
- **Animations**: Framer Motion
- **HTTP Client**: Axios

**Why This Stack:**

- Fast development and HMR with Vite
- Beautiful animations for user engagement
- Responsive design for all devices
- Real-time analysis feedback

**Key Features:**

- Resume upload and parsing
- Job description matching
- ATS score calculation
- Skill gap analysis
- Real-time feedback and suggestions

---

### 7. **Buffer Memory** (`buffer_memory/`)

**Purpose:** Simple conversation memory system  
**Technologies:**

- Python classes for memory management
- Text file persistence
- Conversation history tracking

**Why This Approach:**

- Lightweight memory system
- Perfect for simple chatbots
- Persistent conversation history

**Key Features:**

- Store and retrieve chat messages
- Simple memory window

---

### 8. **PDF Summary** (`pdf_summary/`)

**Purpose:** Automatic summarization of PDF documents  
**Models & Technologies:**

- **Summarization**: Uses transformers-based models
- **PDF Processing**: pypdf extraction
- **Chunking**: Document splitting for long PDFs
- **Memory**: Persistent storage of summaries

**Key Features:**

- Extract text from PDFs
- Generate concise summaries
- Store summaries for later reference

---

### 9. **Resume Chatbot** (`resume_chatbot/`)

**Purpose:** Interactive chatbot trained on resume data  
**Technologies:**

- Resume parsing
- Conversation management
- Context retention

**Key Features:**

- Answer questions about resume
- Extract specific information
- Retrieve experience details

---

### 10. **Summary Memory** (`summary_memory/`)

**Purpose:** Advanced document summarization with persistent memory  
**Models & Technologies:**

- **Model**: `facebook/bart-large-cnn`
- **Framework**: Transformers (Hugging Face)
- **File Support**: PDF, TXT, DOCX, CSV
- **Chunking**: Recursive text splitting

**Why BART Large CNN:**

- Specifically trained on news summarization (high quality)
- Abstractive summarization (not just extraction)
- Good balance of model size and performance
- Handles various document lengths

**Configuration:**

- Chunk Size: 3000 tokens
- Max Summary Length: 200 tokens
- Min Summary Length: 50 tokens

**Key Features:**

- Multi-format document support
- Extractive summarization
- Persistent memory system
- Token-based chunking

---

### 11. **Summary Memory Bot** (`summary_memory_bot/`)

**Purpose:** Conversational interface for document summarization  
**Technologies:**

- Memory management
- Conversation history
- Summarization pipeline

**Key Features:**

- Interactive summarization
- Chat-based interface
- Memory persistence

---

### 12. **Window Memory** (`window_memory/`)

**Purpose:** Sliding window memory management for conversations  
**Technologies:**

- Window-based message storage
- Configurable memory size
- Text persistence

**Why Window Memory:**

- Efficient for long conversations
- Maintains context within window
- Prevents memory overflow
- Lower computational cost

**Key Features:**

- Fixed-size conversation window
- Sliding window mechanism
- Memory bounds

---

### 13. **Practice/AI Research Agent** (`Practice/ai_research_agent/`)

**Purpose:** ReAct (Reasoning + Acting) agent for research tasks  
**Models & Technologies:**

- **Pattern**: ReAct framework (Reason → Act → Observe)
- **Tools**: Web search, information gathering
- **Memory**: Conversation state management

**Why ReAct:**

- Combines reasoning with tool usage
- Interpretable decision-making
- Better for complex multi-step tasks
- Emerging pattern for agentic AI

**Key Features:**

- Autonomous research capabilities
- Tool integration
- Reasoning traces
- Report generation

---

### 14. **Practice/Text to Speech** (`Practice/Text_to_speech/`)

**Purpose:** Text-to-speech synthesis system  
**Technologies:**

- TTS Engine: gTTS or similar
- Audio generation and playback
- Voice customization

**Key Features:**

- Convert text to natural speech
- Multiple language support
- Audio file generation

---

## 🏗️ Architecture Patterns

### RAG (Retrieval-Augmented Generation)

Used in: RAG Chatbot, Interview Agent, Resume Analyzer

```
Document → Chunk → Embed → Store → Query → Retrieve → LLM → Answer
```

### Memory Systems

- **Buffer Memory**: Simple conversation history
- **Window Memory**: Sliding context window
- **Summary Memory**: Compressed long-term memory with abstractions

### Embedding Models Comparison

| Model                  | Size | Speed  | Accuracy   | Use Case                                 |
| ---------------------- | ---- | ------ | ---------- | ---------------------------------------- |
| all-MiniLM-L6-v2       | 22MB | ⚡⚡⚡ | ⭐⭐⭐⭐   | General semantic search, resume matching |
| BAAI/bge-small-en-v1.5 | 33MB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Document retrieval, best performance     |

### LLM Models

| Model        | Parameters | Speed    | Quality | Use Case                    |
| ------------ | ---------- | -------- | ------- | --------------------------- |
| SmolLM2-360M | 360M       | ⚡⚡⚡⚡ | ⭐⭐⭐  | Lightweight QA, mobile/edge |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment (venv)
- Git

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

### Running Projects

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

**ResumePilot AI:**

```bash
# Terminal 1 - Backend
cd ResumePilot_AI/Backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd ResumePilot_AI/Frontend
npm install
npm run dev
```

**Attendance Agent:**

```bash
cd Attendece_agent
python main.py
```

---

## 📚 Model Selection Guide

### When to use which embedding model?

- **all-MiniLM-L6-v2**: Resume matching, general search, mobile deployment
- **BAAI/bge-small-en-v1.5**: Production RAG systems, document retrieval, maximum accuracy

### When to use which summarization model?

- **BART Large CNN**: News articles, formal documents, high-quality abstracts
- **T5**: General-purpose summarization, multilingual support

### When to use which LLM?

- **SmolLM2-360M**: Edge devices, fast inference, local deployment
- **Claude/GPT-4** (via API): Complex reasoning, production applications
- **Llama 2**: Open-source, self-hosted option

---

## 🔧 Configuration

Key configuration files:

- `Day-5/Embedding/config.py`: Embedding model settings
- `summary_memory/config.py`: Summarization parameters
- `LangChain_models/rag-chatbot/src/llm.py`: LLM configuration
- `.env`: API keys and secrets (not in repo for security)

---

## 📝 Project Structure

```
Agentic_AWS/
├── Attendece_agent/          # Attendance analysis system
├── Day-5/Embedding/          # Semantic memory system
├── Interview_agent/          # RAG-based interview system
├── LangChain_models/         # RAG chatbot implementation
├── Practice/                 # Experimental agents and demos
├── ResumePilot_AI/          # Full-stack resume platform
├── Resume_Analyser/          # Resume-JD matching
├── buffer_memory/            # Simple memory system
├── pdf_summary/              # PDF summarization
├── summary_memory/           # Advanced memory with summaries
└── window_memory/            # Sliding window memory
```

---

## 🎯 Key Technologies & Libraries

- **LLM Frameworks**: LangChain, Transformers, Sentence Transformers
- **Vector Databases**: FAISS
- **Web Frameworks**: FastAPI, Streamlit, React
- **Data Processing**: pandas, PyPDF, docx2txt
- **Speech**: gTTS, speech_recognition
- **Frontend**: React, Tailwind CSS, Framer Motion

---

## 🔮 Future Enhancements

1. Integration with production LLMs (Claude, GPT-4, Bedrock)
2. Multi-language support across all agents
3. Advanced memory management (semantic deduplication)
4. Real-time streaming responses
5. Advanced RAG (multi-hop reasoning, hybrid search)
6. User authentication and role-based access
7. Analytics and performance monitoring
8. Deployment to AWS services (Lambda, SageMaker)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Satyam Diwaker**  
GitHub: [@Satyamdiwaker000001](https://github.com/Satyamdiwaker000001)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For questions and support, please open an issue on GitHub or contact the author.

---

**Last Updated**: June 2026  
**Status**: Active Development
