# ============================================================
# TRAVEL RAG AGENT - STREAMLIT APP
# ============================================================

import streamlit as st

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

    st.header("📊 Dashboard")

    stats = dashboard_statistics(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Records",
            stats["total_records"]
        )

    with col2:
        st.metric(
            "Destinations",
            stats["total_destinations"]
        )

    with col3:
        st.metric(
            "Average Duration",
            stats["average_duration"]
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "Avg Accommodation Cost",
            stats["average_accommodation_cost"]
        )

    with col5:
        st.metric(
            "Avg Transportation Cost",
            stats["average_transportation_cost"]
        )

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

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