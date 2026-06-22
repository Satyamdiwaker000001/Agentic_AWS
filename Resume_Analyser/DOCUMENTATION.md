# Resume Analyzer - Documentation

## 1. What does the project do?
This project is an automated resume matcher. It evaluates a list of candidate resumes (PDF format) against a predefined Job Description (`jd.txt`) using semantic similarity, calculates match percentages, and displays ranked candidate profiles on the terminal console.

## 2. What is the request flow?
1. **Model Initialization**: The script loads the sentence transformer embedding model `all-MiniLM-L6-v2`.
2. **Read JD**: The contents of the target Job Description file `jd.txt` are read.
3. **Embed JD**: The job description string is encoded into a vector representation.
4. **Traverse Resumes**: The script loops over all files in the `resumes/` folder.
5. **Parse PDF**: For each PDF resume, `pypdf.PdfReader` extracts page texts.
6. **Embed Resume**: The extracted resume text is encoded into a vector representation.
7. **Similarity Calculation**: Cosine similarity is computed between the JD vector and the resume vector to generate a match score.
8. **Ranking & Display**: The results are converted to percentages, sorted in descending order, and printed to the terminal console as a ranked list.

## 3. Which packages are used and why?
- **`sentence-transformers`**: Provides the `all-MiniLM-L6-v2` encoder model to calculate semantic representations of JD and resume files.
- **`scikit-learn`**: Computes the `cosine_similarity` score between the generated vectors.
- **`pypdf`**: Extracts text from PDF candidate resume profiles.
- **`os`** (standard library): Handles directory listings and file operations.

## 4. Where does the data come from?
- Job requirements: `jd.txt` file content.
- Candidate profiles: PDF resumes loaded from the `resumes/` directory.

## 5. Where is the data stored?
All evaluations, vector encodings, and calculations are stored in RAM variables at runtime. No persistent database or output report files are created.

## 6. What is the role of the LLM?
There is no generative chat LLM. An embedding model (`all-MiniLM-L6-v2`) is used to convert textual descriptions into vector coordinate structures to perform mathematical similarity matching.

## 7. What breaks if the LLM is removed?
If the sentence-transformer models are removed, the vector similarity matching pipeline will break. The code would need to fall back to a basic string keyword matching or token frequency overlap checks.
