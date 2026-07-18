# app.py
# Interactive dashboard UI for the Offline SRS Compliance Analyzer.

import os
import tempfile
import pandas as pd
import streamlit as st

from parser import parse_document
from analyzer import SRSAnalyzer
from standards import STANDARDS

# Custom UI helpers
from frontend.custom_components import load_css, top_navbar, apply_theme

def generate_srs_template(standard_id):
    """Generates a blank skeleton template for the chosen standard."""
    standard_def = STANDARDS[standard_id]
    template_lines = []
    template_lines.append(f"# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)")
    template_lines.append(f"# Framework: {standard_def['title']}")
    template_lines.append(f"# Generated offline by SRS Compliance Analyzer\n")
    template_lines.append("## Project Name: [Insert Project Name]")
    template_lines.append("## Version: 1.0")
    template_lines.append("## Date: [Insert Date]\n")
    template_lines.append("=" * 60 + "\n")
    
    for sec in standard_def["sections"]:
        indent = "  " * (len(sec["id"].split(".")) - 1)
        req = " (Required)" if sec["required"] else " (Optional)"
        template_lines.append(f"{indent}{sec['id']} {sec['name']}{req}")
        template_lines.append(f"{indent}[Write description and specification requirements here...]\n")
        
    return "\n".join(template_lines)

# Set Page Config with SEO metadata
st.set_page_config(
    page_title="Offline SRS Compliance Analyzer & Auditor",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# End of page config

# Lazy-load analyzer in session state
if "analyzer" not in st.session_state:
    with st.spinner("Spawning local sentence embeddings pipeline (MiniLM)..."):
        st.session_state.analyzer = SRSAnalyzer()

analyzer = st.session_state.analyzer

# Wrapper for entire app
st.markdown("<div class='main-wrapper'>", unsafe_allow_html=True)
load_css()
top_navbar()

# Layout: 70% left (content), 30% right (overview)
col_main, col_side = st.columns([7, 3])

with col_main:
    st.markdown("<div style='padding: 2rem;'>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>SRS Standard Configuration</div>", unsafe_allow_html=True)
    selected_standard_id = st.selectbox(
        "Choose target standard:",
        list(STANDARDS.keys()),
        format_func=lambda x: STANDARDS[x]["title"]
    )
    standard_def = STANDARDS[selected_standard_id]
    
    st.markdown(f"<div class='section-body'>{standard_def['description']}</div>", unsafe_allow_html=True)
    
    template_txt = generate_srs_template(selected_standard_id)
    st.download_button(
        label="➕ Download Blank Template",
        data=template_txt,
        file_name=f"{selected_standard_id}_Template.txt",
        mime="text/plain",
        help="Download a clean starter requirements skeleton of the selected standard.",
        use_container_width=True
    )
    
    st.markdown("<div class='section-header'>Document Upload</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Your position here, Company here - Upload SRS Document (.pdf, .docx, .txt)",
        type=["pdf", "docx", "txt"],
        key="srs_file_uploader"
    )
    
    results = None
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_filepath = tmp_file.name

        try:
            from parser import parse_document_to_blocks
            document_blocks = parse_document_to_blocks(temp_filepath)
            total_chars = sum(len(b["text"]) for b in document_blocks)

            if total_chars < 100:
                st.error("Document is too short or has no extractable text.")
            else:
                results = analyzer.analyze_compliance(document_blocks, standard_def)
        except Exception as e:
            st.error(f"Error analyzing document: {e}")
        finally:
            if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
                os.remove(temp_filepath)
                
    # Chat integration
    st.markdown("<div class='section-header'>AI Assistant Chat</div>", unsafe_allow_html=True)
    from agent import get_agent
    chat_agent = get_agent()
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    user_input = st.text_input("Ask a question about your SRS document", key="chat_input")
    if st.button("Send Message") and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = chat_agent.generate(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")

    st.markdown("</div>", unsafe_allow_html=True)

with col_side:
    st.markdown("<div class='overview-panel'>", unsafe_allow_html=True)
    st.markdown("<h3>Overview</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666; font-size:0.9rem;'>Welcome to your SRS document review!</p>", unsafe_allow_html=True)
    
    if results:
        score = results["score"]
        sections = results["sections"]
        matched = sum(1 for sec in sections.values() if sec["status"] == "Matched")
        weak = sum(1 for sec in sections.values() if sec["status"] == "Weak")
        missing = sum(1 for sec in sections.values() if sec["status"] == "Missing")
        
        # Circular progress mock
        st.markdown(f"""
        <div class="score-ring">
            {score}%
        </div>
        <p style='text-align:center; font-size:0.9rem; font-weight:600; margin-bottom:2rem;'>Your document scored {score} out of 100</p>
        """, unsafe_allow_html=True)
        
        # Grid metrics
        st.markdown(f"""
        <div class="metric-grid">
            <div class="mini-metric-card">
                <div class="label">Matched</div>
                <div class="value">{matched} <span class="badge-tag tag-excellent">EXCELLENT</span></div>
            </div>
            <div class="mini-metric-card">
                <div class="label">Weak</div>
                <div class="value">{weak} <span class="badge-tag tag-average">AVERAGE</span></div>
            </div>
            <div class="mini-metric-card">
                <div class="label">Missing</div>
                <div class="value">{missing} <span class="badge-tag tag-average">POOR</span></div>
            </div>
            <div class="mini-metric-card">
                <div class="label">Total Sections</div>
                <div class="value">{len(sections)} <span class="badge-tag tag-good">GOOD</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # List breakdown
        list_html = ""
        for sec_id, data in sections.items():
            status = data["status"]
            score_text = "10/10" if status == "Matched" else ("5/10" if status == "Weak" else "0/10")
            list_html += f"""
            <div class="list-item">
                <span style="font-weight:500;">{data['name']}</span>
                <span class="score">{score_text}</span>
            </div>
            """
        st.markdown(list_html, unsafe_allow_html=True)
        
    else:
        st.markdown("<p style='text-align:center; color:#999; margin-top:3rem;'>Upload a document to see your score overview.</p>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
