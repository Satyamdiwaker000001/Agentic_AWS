# Summary Memory - Documentation

## 1. What does the project do?
This project is an automated document summarization pipeline. It loads files of various formats (PDF, DOCX, CSV, TXT), extracts their text, splits the text into chunks, generates abstractive summaries using the BART model, and appends the summaries to a local text log.

## 2. What is the request flow?
1. **Execution Start**: The user runs `main.py`.
2. **File Loading**: The script reads the target file `documents/cpp.pdf`.
3. **Dynamic Parsing**: `loaders.py` extracts text based on the file extension:
   - `.pdf`: Page texts are extracted using `pypdf.PdfReader`.
   - `.docx`: Paragraphs are extracted using `python-docx`.
   - `.csv`: Tabular data is parsed using `pandas` and converted to string.
   - `.txt`: Standard read operations.
4. **Text Summarization**:
   - The extracted text is passed to `summarize_document()`.
   - The text is split into chunks of character size `CHUNK_SIZE = 3000`.
   - Each chunk is passed to the HuggingFace summarization pipeline using `facebook/bart-large-cnn` to generate abstractive summaries.
   - The chunk summaries are concatenated.
5. **Memory Saving**: `SummaryMemory.save()` appends the generated summaries to `summary_memory.txt`.

## 3. Which packages are used and why?
- **`pypdf`**: Extracts text from PDF files.
- **`python-docx`**: Parses paragraphs and text formatting from Word DOCX files.
- **`pandas`**: Loads and processes CSV files.
- **`transformers`** (HuggingFace): Loads and runs the deep learning Seq2Seq summarization model pipeline (`facebook/bart-large-cnn`).

## 4. Where does the data come from?
The data is read from local document files located under the `documents/` directory.

## 5. Where is the data stored?
The summarized text is appended to a local flat text file: `summary_memory.txt`.

## 6. What is the role of the LLM?
A Seq2Seq abstractive summarization model (`facebook/bart-large-cnn`) is used to compress large document chunks into concise, cohesive paragraphs.

## 7. What breaks if the LLM is removed?
The core summarization engine will break, and the script will throw exceptions. The system would need a fallback algorithm based on simple character slicing or sentence extraction metrics.
