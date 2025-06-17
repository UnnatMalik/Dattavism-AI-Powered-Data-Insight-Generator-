from flask import session
import streamlit as st 
import pandas as pd
from utils.gemini_ai import context_detection, generate_report

st.set_page_config(
    page_title="Upload Data-Sets",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="expanded",
)

class Pages_switch():
    st.sidebar.page_link("main.py", label="Home 🏠")
    st.sidebar.page_link("pages/upload_data.py", label="Upload Data-Sets 📂")
    st.sidebar.page_link("pages/report.py", label="Data-Set report 📄")

st.title("📂 Upload Your Dataset")
st.markdown("Upload a CSV file from any domain (e.g., business, healthcare, research) and let the AI generate insights.")

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"],
    help="Upload a CSV file to analyze. The file should contain structured data with headers.",
)

if uploaded_file is not None:
    try : 
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df
        st.session_state["filename"] = uploaded_file.name.strip(".csv")
        st.success("File uploaded successfully!") 
        st.write("### Preview of Dataset:")
        st.write(df.head())
        st.write("### Dataset Summary:")
        st.write(df.describe())
    except Exception as e:
        st.error(f"Error reading the file: {e}")

    st.button("Send For analysis",
        help="Click to send the uploaded dataset for analysis. The AI will generate insights and visualizations based on the data.",
        on_click=lambda: st.toast("Dataset sent for analysis! Please wait for the report.",icon="📄")
    )
    st.markdown("---")
    

