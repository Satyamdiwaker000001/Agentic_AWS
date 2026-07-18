import streamlit as st
import os

def load_css():
    css_path = os.path.join('frontend', 'styles.css')
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def top_navbar():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        logo_path = os.path.join('frontend', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            st.image(logo_path, width=48)
    with col2:
        st.markdown("<h1 style='color:#fff; margin:0;'>SRS Compliance Analyzer</h1>", unsafe_allow_html=True)
    with col3:
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
        if st.button('🌙' if st.session_state.theme == 'light' else '☀️'):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.experimental_set_query_params(theme=st.session_state.theme)

def apply_theme():
    theme = st.session_state.get('theme', 'light')
    if theme == 'dark':
        st.markdown("<script>document.documentElement.setAttribute('data-theme','dark');</script>", unsafe_allow_html=True)
    else:
        st.markdown("<script>document.documentElement.removeAttribute('data-theme');</script>", unsafe_allow_html=True)
