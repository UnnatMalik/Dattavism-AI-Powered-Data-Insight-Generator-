import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import requests
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Dattavism",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


    # st.sidebar.page_link("pages/Live_track.py", label="Live Track 📈")
# ---------- LOAD LOTTIE ANIMATION ----------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json")  # AI animation

class Pages_switch():
    st.sidebar.page_link("main.py", label="Home 🏠")
    st.sidebar.page_link("pages/upload_data.py", label="Upload Data-Sets 📂")
    st.sidebar.page_link("pages/report.py", label="Data-Set report 📄")
    st.sidebar.page_link("pages/Q&A.py", label="Q&A with Dattavism ❓")


# ---------- TITLE & HEADER ----------
st.markdown("""
    <style>
        .title {font-size: 50px; font-weight: 700; color: #f9fafc;}
        .tagline {font-size: 20px; color: #ccc;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📊 DATTAVISM AI-Powered Data Insight Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>Analyze any dataset using Gemini, Pandas, Matplotlib & Streamlit</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- LAYOUT ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🤖 What does this app do?")
    st.markdown("""
    - Upload any `.csv` file related to **finance**, **research**, **medical**, **sales**, or **science**.
    - It **analyzes**, **detects context**, **summarizes**, and **visualizes** your data automatically using:
        - 🧠 Gemini (AI summary + Q&A)
        - 📊 Matplotlib for graphs
        - 🧮 Pandas + NumPy for profiling
        - 💾 MySQL (optional session tracking)
    """)
    st.success("➡️ Use the **sidebar** to begin by uploading your data.")

with col2:
    st_lottie(lottie_ai, height=280, key="ai")

# ---------- FEATURE CARDS ----------
# ---------- FEATURE SECTION (REPLACE THIS BLOCK) ----------
st.markdown("""
<style>


/* Individual feature card */
.feature-card {
    background: linear-gradient(120deg,#212225 0%,#2e3035 100%);
    padding: 30px 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    transition: transform .25s ease, box-shadow .25s ease;
}

/* Hover lift */
.feature-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 8px 18px rgba(0,0,0,0.5);
}

/* Title + text */
.feature-title  {font-size: 22px; font-weight: 600; color:#fafafa; margin-bottom:10px;}
.feature-desc   {font-size: 15px; color:#d0d0d0; line-height:1.5;}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='feature-band'>", unsafe_allow_html=True)

    # Use a 3‑column grid; breakpoint automatically collapses on small screens
    col_a, col_b, col_c = st.columns(3, gap="large")

    with col_a:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-title'>📂 Upload Any CSV</div>
            <div class='feature-desc'>Load structured data from <i>any</i> domain and kick‑start your analysis.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card' style='margin-top:25px;'>
            <div class='feature-title'>🧮 Data Profiling</div>
            <div class='feature-desc'>Automatic schema, nulls, statistics &amp; type detection.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-title'>🧠 AI Context Detection</div>
            <div class='feature-desc'>Gemini figures out what the dataset represents—business KPIs, clinical trials, research logs, you name it.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card' style='margin-top:25px;'>
            <div class='feature-title'>📈 Auto Visualisations</div>
            <div class='feature-desc'>Instant, clean charts driven by Matplotlib &amp; your data’s shape.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-title'>💬 Ask Dattavism</div>
            <div class='feature-desc'>Type questions in natural language and get data‑aware answers.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card' style='margin-top:25px;'>
            <div class='feature-title'>📤 Export Report</div>
            <div class='feature-desc'>Download AI summaries and visualisations in PDF or text form, or revisit them later.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
# ---------- END FEATURE SECTION ----------


# ---------- QUICK START ----------
st.markdown("### 🚀 Quick Start")
st.info("""
1. Head to **1_Upload_Data** from the sidebar.
2. Upload your CSV.
3. Explore insights across:
   - 🧮 Profiling
   - 📊 Visuals
   - 🤖 Ask Gemini
   - 📤 Export
""")

# ---------- SAMPLE CSV DOWNLOAD ----------
with st.expander("📎 Need a sample dataset?"):
    st.download_button(
        label="Download Sample CSV",
        data="""Name,Age,Salary\nAlice,25,50000\nBob,30,60000\nCharlie,35,70000""",
        file_name="sample_data.csv",
        mime="text/csv"
    )

# ---------- FOOTER ----------
st.markdown("---")
st.caption(f"🧠 Powered by Python • Gemini • Streamlit • Matplotlib | Last updated {datetime.now().strftime('%Y-%m-%d')}")
