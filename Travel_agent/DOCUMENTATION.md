# Travel Agent - Documentation

## 1. What does the project do?
This project is an AI-powered travel assistant and analytics dashboard (Travel Agent OS). It uses a local dataset (`Travel details dataset.csv`) to show historical travel metrics, train a Random Forest regression model to predict trip costs, and run a local RAG pipeline to answer user travel queries and formulate personalized recommendations.

## 2. What is the request flow?
1. **Startup & Initialization**:
   - The user runs `streamlit run app.py`.
   - `initialize_project()` loads, validates, and cleans the CSV dataset (`data_engine.py`).
   - Clean rows are converted to LangChain Document format (`rag_engine.py`).
   - A Chroma vector database index is built or loaded from `./vectorstore` using HuggingFaceEmbeddings (`all-MiniLM-L6-v2`).
   - A Random Forest regression model is trained on duration and destination features to predict total travel costs (`recommendation_engine.py`).
2. **Dashboard Interactive Flow**:
   - **Dashboard Option**: Displays global metrics, Plotly charts, demographics pie charts, and average costs.
   - **Travel AI Option**: The user inputs a chat query. ChromaDB retrieves top similar document snippets (`k=5`). A prompt combining context and query is sent to the local `SmolLM2-135M-Instruct` model to generate a response.
   - **Recommendations Option**: The user submits trip parameters (budget, duration, gender counts, relationship). The system filters matching rows via budget constraints, and the local LLM generates a personalized itinerary.
   - **Cost Prediction Option**: The user selects a destination and duration. The trained RandomForest model estimates and displays the projected cost.
   - **Analytics Option**: Renders gender-based top destinations and nationality distributions.

## 3. Which packages are used and why?
- **`streamlit` & `streamlit-option-menu`**: Build the interactive web UI and sidebar navigation.
- **`plotly`**: Generates high-quality interactive charts, pie graphs, and treemaps.
- **`pandas`**: Handles dataset loading, cleaning, filtering, and aggregation.
- **`scikit-learn`**: Trains the `RandomForestRegressor` and encodes categorical labels with `LabelEncoder`.
- **`langchain-huggingface` & `langchain-chroma`**: Integrates HuggingFace embeddings (`all-MiniLM-L6-v2`) and manages the local `Chroma` database.
- **`transformers`**: Loads and runs the local text-generation pipeline (`SmolLM2-135M-Instruct`).

## 4. Where does the data come from?
- Historical logs: Local dataset file `Travel details dataset.csv`.
- Interactive parameters: User inputs submitted via the Streamlit UI.

## 5. Where is the data stored?
- Vector database: Saved locally under the `./vectorstore/` directory.
- Model weights & system state: Cached dynamically in RAM variables.

## 6. What is the role of the LLM?
The local LLM (`SmolLM2-135M-Instruct`) parses retrieved database context to answer travel questions, evaluate queries, and compile custom travel plans.

## 7. What breaks if the LLM is removed?
The Travel AI chatbot and the personalized AI recommendation feature will break completely. However, the analytics dashboards, Plotly charts, budget filters, and Random Forest cost estimator will continue to function standalone.
