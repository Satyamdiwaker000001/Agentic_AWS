# PDF Summary - Documentation

## 1. What does the project do?
This project reads a local PDF file, extracts its textual content page-by-page, and writes the entire parsed text into a local log file `summary_memory.txt`.

## 2. What is the request flow?
1. **Execution Start**: The user runs `main.py`.
2. **Text Extraction**: The script reads the hardcoded path `pdfs/cpp.pdf`. `pdf_reader.py` loops over each page using `pypdf`, extracts the text, and prefixes it with page markers (`===== PAGE {page_num} =====`).
3. **Save**: `SummaryMemory.save` writes the formatted text directly to `summary_memory.txt`, overwriting any previous content.
4. **Complete**: A console print statement confirms that the extraction is complete.

## 3. Which packages are used and why?
- **`pypdf`**: Used to read PDF pages and extract their text content.

## 4. Where does the data come from?
The data comes from a local PDF file: `pdfs/cpp.pdf`.

## 5. Where is the data stored?
The extracted text is written to a local flat text file: `summary_memory.txt`.

## 6. What is the role of the LLM?
There is **no LLM model used** in this project. The `summarizer.py` file contains a helper function `summarize_text` which simply slices a substring based on character count.

## 7. What breaks if the LLM is removed?
**Nothing breaks**, since the project has no AI model dependencies.
