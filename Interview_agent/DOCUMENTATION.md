# Interview Agent - Documentation

## 1. What does the project do?
This project is an AI-powered voice-based technical interview simulator. It extracts text from a candidate's PDF resume, builds a semantic search index, generates contextual interview questions, speaks them out loud, records the candidate's audio responses, transcribes the voice inputs into text, and provides automated scoring and detailed feedback.

## 2. What is the request flow?
1. **Resume Processing**: `rag/parser.py` uses PyMuPDF (fitz) to extract text from `resumes/resume.pdf`.
2. **Text Chunking**: The extracted text is split into segments using character length thresholds (`rag/embeddings.py`).
3. **Index Creation**: The segments are encoded using `all-MiniLM-L6-v2` and added to a FAISS in-memory index (`rag/vector_store.py`).
4. **Interview Loop**:
   - The script queries the FAISS index for "project experience" to retrieve matching candidate chunks.
   - The retrieved context is formatted into a prompt and sent to the local LLM (`models/qwen.gguf` loaded via `llama_cpp`) to generate a single interview question.
   - The generated question is spoken out loud using `gTTS` and played via `os.system("start ...")`.
   - The candidate's response is recorded for 20 seconds using the `sounddevice` library and saved as `audio/answer.wav`.
   - The saved WAV file is transcribed to text using the local `faster_whisper` Tiny model.
   - The transcribed answer and question are sent to the local LLM for evaluation, outputting a score (X/10) and feedback.

## 3. Which packages are used and why?
- **`llama-cpp-python` (`llama_cpp`)**: Runs the local instruct model (`models/qwen.gguf`) on CPU/GPU for question generation and candidate evaluation.
- **`sentence-transformers`**: Generates text embeddings for vector indexing.
- **`faiss-cpu`**: Fast, lightweight library for vector similarity search.
- **`PyMuPDF` (`fitz`)**: Parses and extracts textual content from PDF files.
- **`gTTS`**: Google Text-to-Speech engine to convert text questions to MP3 files.
- **`faster-whisper`**: High-performance local speech-to-text transcriber to process recorded candidate answers.
- **`sounddevice` & `scipy`**: Capture hardware microphone streams and write raw audio files.

## 4. Where does the data come from?
- Candidate profile: PDF file `resumes/resume.pdf`.
- Candidate responses: Spoken voice inputs recorded via user's microphone.

## 5. Where is the data stored?
- Generated questions audio: `audio/question.mp3`.
- Candidate microphone recording: `audio/answer.wav`.
- Database vectors: Stored in RAM within the in-memory FAISS index variables.

## 6. What is the role of the LLM?
The local LLM (`Qwen` model run via `llama_cpp`) plays a dual role:
1. Synthesizes relevant interview questions based on resume text snippets retrieved from the FAISS database.
2. Evaluates transcription responses and generates structured grading scores and actionable feedback.

## 7. What breaks if the LLM is removed?
If the LLM is removed, the dynamic interview question generation and response evaluation features will break completely. The pipeline will not be able to formulate logical interview loops or grade answers.
