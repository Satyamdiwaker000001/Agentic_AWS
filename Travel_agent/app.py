# ============================================================
# TRAVEL RAG AGENT - STREAMLIT APP
# ============================================================

import streamlit as st
import pandas as pd

from data_engine import (
    load_dataset,
    validate_dataset,
    clean_dataset
)

from rag_engine import (
    create_documents,
    build_vectorstore
)

from ai_engine import (
    ask_travel_ai,
    recommend_trip
)

from recommendation_engine import (
    recommend_by_budget,
    cheapest_destinations,
    train_cost_model,
    predict_trip_cost
)

from analytics_engine import (
    gender_analysis,
    nationality_analysis,
    dashboard_statistics
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Travel RAG Agent",
    page_icon="✈️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================

st.markdown("""
<style>
/* Animated Gradient Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0b0c10, #1f2833, #0b0c10, #45a29e);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #c5c6c7;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: rgba(11, 12, 16, 0.85) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(102, 252, 241, 0.2);
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background: rgba(31, 40, 51, 0.6);
    border: 1px solid rgba(102, 252, 241, 0.3);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(4px);
    transition: all 0.3s ease-in-out;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-5px) scale(1.02);
    border-color: #66fcf1;
    box-shadow: 0 8px 32px 0 rgba(102, 252, 241, 0.2);
}

/* Headers */
h1, h2, h3 {
    color: #66fcf1 !important;
    font-family: 'Inter', sans-serif;
    text-shadow: 0px 0px 8px rgba(102, 252, 241, 0.4);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #45a29e, #66fcf1);
    color: #0b0c10 !important;
    font-weight: bold;
    border: none;
    border-radius: 25px;
    padding: 0.5rem 2rem;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #66fcf1, #45a29e);
    box-shadow: 0 0 15px rgba(102, 252, 241, 0.6);
    transform: scale(1.05);
}

/* Text area and inputs */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
    background-color: rgba(31, 40, 51, 0.7) !important;
    color: white !important;
    border: 1px solid rgba(102, 252, 241, 0.3) !important;
    border-radius: 8px;
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: #66fcf1 !important;
    box-shadow: 0 0 8px rgba(102, 252, 241, 0.5) !important;
}

/* Success/Warning messages */
.stAlert {
    background-color: rgba(31, 40, 51, 0.8) !important;
    border: 1px solid rgba(102, 252, 241, 0.5) !important;
    color: white !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_resource
def initialize_project():

    file_path = "Travel details dataset.csv"

    df = load_dataset(file_path)

    if df is None:
        return None

    if not validate_dataset(df):
        return None

    df = clean_dataset(df)

    documents = create_documents(df)

    build_vectorstore(documents)

    model, encoder = train_cost_model(df)

    return {
        "df": df,
        "model": model,
        "encoder": encoder
    }


project = initialize_project()

if project is None:
    st.error("Dataset Initialization Failed")
    st.stop()

df = project["df"]
model = project["model"]
encoder = project["encoder"]

# ============================================================
# TITLE
# ============================================================

st.title("✈️ Travel RAG Agent")

st.markdown(
    """
    Ask travel questions, analyze travel trends,
    get destination recommendations, and predict trip costs.
    """
)

# ============================================================
# SIDEBAR
# ============================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Travel AI",
        "Recommendations",
        "Cost Prediction",
        "Analytics"
    ]
)

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("📊 Executive Dashboard")
    st.markdown("Overview of travel data and key metrics.")

    stats = dashboard_statistics(df)

    # Top Row Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trips", stats["total_records"])
    with col2:
        st.metric("Destinations", stats["total_destinations"])
    with col3:
        st.metric("Avg Accom. Cost", f"${stats['average_accommodation_cost']}")
    with col4:
        st.metric("Avg Transport Cost", f"${stats['average_transportation_cost']}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Middle Row Charts
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📍 Top 10 Most Visited Destinations")
        top_dest = df['Destination'].value_counts().head(10)
        st.bar_chart(top_dest, color="#66fcf1")

    with col_b:
        st.subheader("👥 Traveler Gender Distribution")
        gender_dist = df['Traveler gender'].value_counts()
        st.bar_chart(gender_dist, color="#45a29e")

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Row Chart
    st.subheader("💰 Average Total Cost by Destination (Top 10)")
    temp_df = df.copy()
    temp_df["Total Cost"] = pd.to_numeric(temp_df["Accommodation cost"], errors='coerce').fillna(0) + pd.to_numeric(temp_df["Transportation cost"], errors='coerce').fillna(0)
    avg_cost = temp_df.groupby('Destination')['Total Cost'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_cost, color="#ff007f")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 View Raw Dataset"):
        st.dataframe(df, width='stretch')

# ============================================================
# TRAVEL AI
# ============================================================

elif page == "Travel AI":

    st.header("🤖 Travel AI")

    query = st.text_area(
        "Ask a travel question"
    )

    if st.button("Get Answer"):

        if query.strip():

            with st.spinner(
                "Generating Answer..."
            ):

                answer = ask_travel_ai(query)

            st.success("Answer")

            st.write(answer)

# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.header("🌍 Destination Recommendations")

    budget = st.number_input(
        "Budget",
        min_value=1000,
        value=50000
    )

    male_count = st.number_input(
        "Male Travelers",
        min_value=0,
        value=1
    )

    female_count = st.number_input(
        "Female Travelers",
        min_value=0,
        value=1
    )

    duration = st.number_input(
        "Duration (Days)",
        min_value=1,
        value=5
    )

    if st.button("Recommend Destination"):

        st.subheader(
            "AI Recommendation"
        )

        recommendation = recommend_trip(
            budget=budget,
            duration=duration,
            male_count=male_count,
            female_count=female_count
        )

        st.write(recommendation)

        st.subheader(
            "Budget Friendly Destinations"
        )

        recommendations = recommend_by_budget(
            df,
            budget
        )

        if recommendations.empty:
            st.warning("No destinations found within this budget.")
        else:
            st.dataframe(
                recommendations.reset_index()
            )

# ============================================================
# COST PREDICTION
# ============================================================

elif page == "Cost Prediction":

    st.header("💰 Cost Prediction")

    destination = st.selectbox(
        "Destination",
        sorted(df["Destination"].unique())
    )

    duration = st.number_input(
        "Duration (Days)",
        min_value=1,
        value=5
    )

    if st.button("Predict Cost"):

        predicted_cost = predict_trip_cost(
            model=model,
            encoder=encoder,
            destination=destination,
            duration=duration
        )

        st.success(
            f"Estimated Trip Cost: {predicted_cost}"
        )

# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    st.header("📈 Travel Analytics")

    tab1, tab2, tab3 = st.tabs(
        [
            "Gender Analysis",
            "Nationality Analysis",
            "Cheapest Destinations"
        ]
    )

    # --------------------------------------------------------

    with tab1:

        result = gender_analysis(df)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Male Travelers",
                result["male_count"]
            )

        with col2:
            st.metric(
                "Female Travelers",
                result["female_count"]
            )

        st.subheader(
            "Top Male Destinations"
        )

        st.json(
            result["male_top_destinations"]
        )

        st.subheader(
            "Top Female Destinations"
        )

        st.json(
            result["female_top_destinations"]
        )

    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "Top Nationalities"
        )

        st.json(
            nationality_analysis(df)
        )

    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "Cheapest Destinations"
        )

        cheapest = cheapest_destinations(df)

        st.dataframe(
            cheapest.reset_index()
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Travel RAG Agent | LangChain + ChromaDB + SmolLM2"
)