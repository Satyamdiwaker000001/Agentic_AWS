# ResumePilot AI - Documentation

## 1. What does the project do?
This project is a full-stack resume analysis and ATS optimization prototype. It features a FastAPI backend and a React + Tailwind CSS frontend. Users upload their PDF resume and submit a Job Description. The application returns detailed analysis, scoring breakdowns, skill alignment charts, and actionable suggestions to optimize the resume for ATS filters.

## 2. What is the request flow?
1. **Frontend Request**: The user fills in forms on the React UI (Job Title, JD text) and uploads a PDF resume.
2. **API Call**: The frontend sends a multipart form POST request to the FastAPI backend endpoints (`/api/analyze` or `/api/score`).
3. **File Buffering**: The backend saves the uploaded PDF file to `app/uploads/` temporarily.
4. **Service Evaluation**: The endpoint calls the `analyze_resume` service module.
5. **Mock Analysis Model**:
   - `app/services/analyzer.py` processes the request using mock scoring logic.
   - It generates dynamic scores, suggestions, technical/soft skill breakdowns, and radar data.
6. **Response & Cleanup**: The backend deletes the temporary upload files and returns the analysis results as JSON.
7. **UI Render**: The React frontend receives the JSON response and dynamically displays the score dashboard, suggestions lists, and Recharts radar/bar graphs.

## 3. Which packages are used and why?
- **Backend (FastAPI)**:
  - `fastapi`: High-performance asynchronous REST API framework.
  - `uvicorn`: ASGI server implementation to run the backend application.
  - `pydantic`: Schema validation and serialization for API responses (`AnalyzeResponse`).
- **Frontend (Vite + React)**:
  - `react`: Renders the single-page interactive application.
  - `tailwindcss`: Modern visual styles and utility classes.
  - `recharts` / `framer-motion`: Interactive charts, radar graphs, and micro-animations.

## 4. Where does the data come from?
The data comes from user inputs (Job Title, JD text) and file uploads (PDF resumes) submitted via the React frontend.

## 5. Where is the data stored?
- Temporary files: Uploaded PDFs are briefly cached in the `app/uploads/` folder.
- SQLite Placeholder: `resumepilot.db` is initialized but not actively integrated into standard routes yet.
- Execution parameters are transient and cleaned up from RAM/disk post response.

## 6. What is the role of the LLM?
In the current baseline prototype, there is no active LLM API integration. It uses mock-based random generators to return structured metrics. The codebase indicates planned integrations with external APIs (OpenAI, Claude, or AWS Bedrock) for production.

## 7. What breaks if the LLM is removed?
Currently, **nothing breaks** in the execution because the AI results are mocked. Once LLM integrations are added, removing the LLM connection will disable live resume scoring and personalized suggestions.
