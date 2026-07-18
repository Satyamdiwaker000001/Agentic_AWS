import streamlit as st
import os

def load_css(css_file: str = "styles.css"):
    """Load a CSS file from the frontend directory and inject it into the Streamlit app.
    The CSS file should be located at `frontend/<css_file>` relative to the project root.
    """
    css_path = os.path.join(os.path.dirname(__file__), css_file)
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file '{css_file}' not found in frontend directory.")

def top_navbar():
    """Render a professional top navigation bar matching the CV Builder design."""
    st.markdown(
        """
        <div class="custom-navbar">
            <div class="nav-left">
                <h2>SRS Analyzer</h2>
            </div>
            <div class="nav-center">
                <div class="search-bar">
                    <span style="margin-right:8px; opacity:0.6;">✨</span>
                    <input type="text" placeholder="Start writing with AI..." disabled />
                    <span style="opacity:0.6;">→</span>
                </div>
            </div>
            <div class="nav-right">
                <span class="preview-mode">Preview Mode <span class="toggle-switch"></span></span>
                <button class="download-btn">Download Report</button>
                <div class="avatar">👨‍💻</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def apply_theme():
    """Inject a minimal dark/light theme CSS that works with the navigation bar.
    Uses a data attribute on <body> to switch themes.
    """
    theme_css = """
    <style>
    body[data-theme='dark'] {
        background: #0f0f0f;
        color: #e0e0e0;
    }
    body[data-theme='light'] {
        background: #fafafa;
        color: #202020;
    }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)
