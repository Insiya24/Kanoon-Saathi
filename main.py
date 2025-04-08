import streamlit as st
from features.case_prioritization import case_prioritization_tab
from features.citizen_and_law import citizen_law_basic, citizen_law_full_chat
from features.legal_research import legal_research_app
from features.bail_reckoner import bail_reckoner_app
import streamlit as st

import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Law-based Project", layout="wide")

# ---------- STYLING ----------
import os
import base64
from streamlit_lottie import st_lottie
import json

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_law = load_lottiefile("law_justice.json")
st_lottie(lottie_law, height=300, key="law")


def set_background(jpg_file):
    with open(jpg_file, "rb") as f:
        data = f.read()
    encoded_string = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Path to your local JPG image
jpg_file = "bg.jpg"

# Set the background
set_background(jpg_file)
custom_css = """
<style>
    body {
        background-color: #FFF0DC;
    }

    .main-title {
        font-size: 3em;
        color: #543A14;
    }
    .subtitle {
        font-size: 1.5em;
        color: #131010;
    }
    .feature-card {
        background-color: rgba(255, 240, 220, 0.9);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px #543A14;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "show_tabs" not in st.session_state:
    st.session_state.show_tabs = False

def go_to_features():
    st.session_state.show_tabs = True

# ---------- HOMEPAGE ----------
if not st.session_state.show_tabs:
    st.markdown('<h1 class="main-title">⚖ Welcome to the Law-based Project</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Empowering legal access, transparency, and awareness.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <p>This platform is built to improve legal processes and awareness for both professionals and citizens.</p>
        <ul>
            🔹 Evaluate bail cases effectively
            🔹 Conduct smart AI-powered legal research
            🔹 Prioritize cases with public input
            🔹 Learn your rights and laws simply
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.button("🚀 Explore Features", on_click=go_to_features)

# ---------- FEATURES PAGE ----------
else:
    if "full_chat_mode" in st.session_state and st.session_state.full_chat_mode:
        citizen_law_full_chat()
    else:
        st.markdown('<h1 class="main-title">📚 Law-based Project Dashboard</h1>', unsafe_allow_html=True)
        tabs = st.tabs([
            "📊 Case Prioritization",
            "👨‍⚖️ Citizen & Law Assistant",
            "🔍 Legal Research Engine",
            "📝 Bail Reckoner"
        ])
        with tabs[0]:
            case_prioritization_tab()
        with tabs[1]:
            citizen_law_basic()  # <- show only the basic form
        with tabs[2]:
            legal_research_app()
        with tabs[3]:
            bail_reckoner_app()
