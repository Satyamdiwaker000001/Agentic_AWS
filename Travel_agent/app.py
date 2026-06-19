# ============================================================
# TRAVEL RAG AGENT - STREAMLIT APP
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================

st.markdown("""
<style>
/* Modern SaaS Dark Theme */
:root {
    --primary: #3b82f6;
    --background: #0f172a;
    --surface: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --accent: #10b981;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--background);
    color: var(--text-primary);
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Glassmorphism Metric Cards */
div[data-testid="metric-container"] {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    border-color: rgba(59, 130, 246, 0.4);
}

div[data-testid="metric-container"] > div {
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 8px;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: var(--text-primary);
    font-size: 2rem;
    font-weight: 700;
}

/* Headers */
h1, h2, h3 {
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, sans-serif;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: var(--primary);
    color: white !important;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    transition: background-color 0.2s ease, transform 0.1s ease;
}

.stButton>button:hover {
    background-color: #2563eb;
    transform: translateY(-1px);
}

.stButton>button:active {
    transform: translateY(0px);
}

/* Inputs */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
    background-color: rgba(15, 23, 42, 0.6) !important;
    color: var(--text-primary) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px;
    padding: 0.5rem;
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Chat messages */
.stChatMessage {
    background-color: var(--surface);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_resource(show_spinner="Initializing Database...")
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
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3125/3125713.png", width=60) # Travel Icon placeholder
    st.title("Travel Agent OS")
    st.markdown("<p style='color: #94a3b8; font-size: 0.9em; margin-top: -15px;'>Intelligent Operations</p>", unsafe_allow_html=True)
    st.divider()
    
    page = option_menu(
        menu_title=None,
        options=["Dashboard", "Travel AI", "Recommendations", "Cost Prediction", "Analytics"],
        icons=["house", "robot", "compass", "calculator", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#3b82f6", "font-size": "18px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px 0", "color": "#f8fafc", "--hover-color": "#334155", "border-radius": "8px"},
            "nav-link-selected": {"background-color": "#3b82f6", "color": "white", "font-weight": "600"},
        }
    )

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("Executive Overview")
    st.markdown("<p style='color: #94a3b8;'>Real-time metrics and operational insights.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    stats = dashboard_statistics(df)

    # Top Row Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trips", f"{stats['total_records']:,}")
    with col2:
        st.metric("Destinations", f"{stats['total_destinations']:,}")
    with col3:
        st.metric("Avg Accom. Cost", f"${stats['average_accommodation_cost']:,.2f}")
    with col4:
        st.metric("Avg Transport Cost", f"${stats['average_transportation_cost']:,.2f}")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Middle Row Charts
    col_a, col_b = st.columns([6, 4])

    with col_a:
        st.markdown("### 📍 Top 10 Destinations")
        top_dest = df['Destination'].value_counts().head(10).reset_index()
        top_dest.columns = ['Destination', 'Count']
        
        fig = px.bar(top_dest, x='Count', y='Destination', orientation='h', 
                     color='Count', color_continuous_scale='Blues')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'), margin=dict(l=0, r=0, t=30, b=0),
            yaxis={'categoryorder':'total ascending'},
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("### 👥 Traveler Demographics")
        gender_dist = df['Traveler gender'].value_counts().reset_index()
        gender_dist.columns = ['Gender', 'Count']
        
        fig2 = px.pie(gender_dist, values='Count', names='Gender', hole=0.6,
                      color_discrete_sequence=['#3b82f6', '#10b981', '#6366f1'])
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'), margin=dict(l=0, r=0, t=30, b=0),
            showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Row Chart
    st.markdown("### 💰 Cost Distribution by Destination")
    temp_df = df.copy()
    temp_df["Total Cost"] = pd.to_numeric(temp_df["Accommodation cost"], errors='coerce').fillna(0) + pd.to_numeric(temp_df["Transportation cost"], errors='coerce').fillna(0)
    avg_cost = temp_df.groupby('Destination')['Total Cost'].mean().sort_values(ascending=False).head(15).reset_index()
    
    fig3 = px.bar(avg_cost, x='Destination', y='Total Cost',
                 color='Total Cost', color_continuous_scale='Viridis')
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc'), margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="", yaxis_title="Average Total Cost ($)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 View Raw Travel Dataset"):
        st.dataframe(df, use_container_width=True)

# ============================================================
# TRAVEL AI
# ============================================================

elif page == "Travel AI":

    st.header("🤖 Travel Assistant AI")
    st.markdown("<p style='color: #94a3b8;'>Ask specialized travel questions powered by RAG and SmolLM2.</p>", unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Travel Agent AI. How can I help you plan your next trip?"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask about destinations, budgets, or travel tips..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Analyzing knowledge base..."):
            response = ask_travel_ai(prompt)
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.header("🌍 Smart Recommendations")
    st.markdown("<p style='color: #94a3b8;'>Discover ideal destinations based on your preferences and budget.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        st.markdown("### 📋 Trip Parameters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            budget = st.number_input("Total Budget ($)", min_value=500, value=5000, step=500)
        with col2:
            duration = st.slider("Duration (Days)", min_value=1, max_value=30, value=7)
        with col3:
            group_type = st.selectbox("Group Type", ["Couple", "Friends", "Family", "Colleagues", "Solo"])

        col4, col5 = st.columns(2)
        with col4:
            male_count = st.number_input("Male Travelers", min_value=0, value=1)
        with col5:
            female_count = st.number_input("Female Travelers", min_value=0, value=1)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Recommendations", use_container_width=True):
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.markdown("### ✨ AI Suggestion")
            with st.spinner("Generating personalized suggestion..."):
                recommendation = recommend_trip(
                    budget=budget,
                    duration=duration,
                    male_count=male_count,
                    female_count=female_count,
                    group_type=group_type
                )
                
            st.info(recommendation, icon="🤖")

        with col_res2:
            st.markdown("### 🎯 Data-Backed Options")
            recommendations = recommend_by_budget(df, budget)

            if recommendations.empty:
                st.warning("No destinations found within this budget.", icon="⚠️")
            else:
                rec_df = recommendations.reset_index()
                rec_df.columns = ["Destination", "Avg. Cost ($)"]
                rec_df["Avg. Cost ($)"] = rec_df["Avg. Cost ($)"].apply(lambda x: f"${x:,.2f}")
                st.dataframe(rec_df, use_container_width=True, hide_index=True)

# ============================================================
# COST PREDICTION
# ============================================================

elif page == "Cost Prediction":

    st.header("💰 Predictive Cost Modeling")
    st.markdown("<p style='color: #94a3b8;'>Estimate future trip expenses using Random Forest regression.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Trip Details")
        destination = st.selectbox(
            "Select Destination",
            sorted(df["Destination"].unique())
        )
        
        duration = st.slider(
            "Expected Duration (Days)",
            min_value=1, max_value=60, value=5
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("Run Prediction Model", use_container_width=True)

    with col2:
        st.markdown("### Prediction Results")
        if predict_btn:
            with st.spinner("Calculating via ML model..."):
                predicted_cost = predict_trip_cost(
                    model=model,
                    encoder=encoder,
                    destination=destination,
                    duration=duration
                )
            
            st.success("Analysis Complete!", icon="✅")
            st.metric(label=f"Estimated Cost for {duration} days in {destination}", value=f"${predicted_cost:,.2f}")
        else:
            st.info("Fill out the details on the left and click 'Run Prediction Model' to see the estimate.")

# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    st.header("📈 Deep Analytics")
    st.markdown("<p style='color: #94a3b8;'>Granular breakdown of historical travel patterns.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Gender Analysis", "Demographics", "Budget Analysis"])

    with tab1:
        result = gender_analysis(df)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Male Travelers", result["male_count"])
            st.markdown("**Top Destinations (Male)**")
            st.dataframe(pd.DataFrame(list(result["male_top_destinations"].items()), columns=["Destination", "Visits"]), use_container_width=True, hide_index=True)
            
        with col2:
            st.metric("Total Female Travelers", result["female_count"])
            st.markdown("**Top Destinations (Female)**")
            st.dataframe(pd.DataFrame(list(result["female_top_destinations"].items()), columns=["Destination", "Visits"]), use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### Traveler Nationalities")
        nat_data = nationality_analysis(df)
        nat_df = pd.DataFrame(list(nat_data.items()), columns=["Nationality", "Count"])
        
        fig = px.treemap(nat_df, path=['Nationality'], values='Count',
                         color='Count', color_continuous_scale='Blues')
        fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### Top 10 Most Budget-Friendly Destinations")
        cheapest = cheapest_destinations(df).reset_index()
        cheapest.columns = ["Destination", "Avg Total Cost ($)"]
        
        fig = px.bar(cheapest, x='Destination', y='Avg Total Cost ($)',
                     color='Avg Total Cost ($)', color_continuous_scale='Greens_r')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'), margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.caption("🚀 Powered by Streamlit, LangChain, ChromaDB & SmolLM2 | Professional SaaS Edition")