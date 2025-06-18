import time
import streamlit as st
from utils.gemini_ai import answer_user_query
from utils.visualizer import generate_visualizations


st.set_page_config(
    page_title="Q&A with AI",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="expanded",
)

class Pages_switch():
    st.sidebar.page_link("main.py", label="Home 🏠")
    st.sidebar.page_link("pages/upload_data.py", label="Upload Data-Sets 📂")
    st.sidebar.page_link("pages/report.py", label="Data-Set report 📄")
    st.sidebar.page_link("pages/Q&A.py", label="Q&A with Dattavism ❓")

st.title("Ask Dattavism Questions About Your Dataset and report ❓")
st.markdown(
    "You can ask questions about your dataset and the Dattavism will provide detailed answers based on the analysis."
)

if "df" not in st.session_state or "report" not in st.session_state:
    st.warning("Please upload a dataset first in the Upload Data-Sets page.")
else:
    df = st.session_state["df"]
    report = st.session_state["report"]
    Col1, Col2 = st.columns(2,border=False)
    with Col1:
        with st.expander("## Dataset Preview 🔍"):
            st.write(df.head(10))
        with st.expander("## Report Preview 📄"):
            with st.container(height=500):
                st.write(report)

    with Col2:
        st.write("### Ask your question about the dataset or report:")
        
        user_input = st.chat_input(placeholder="Enter your message")

        with st.container(height=500):
            if "messages" not in st.session_state:
                st.session_state["messages"] = []

            for message in st.session_state["messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_input:
                st.session_state["messages"].append({"role": "user", "content": user_input})
                with st.chat_message('User', avatar="user"):
                    st.markdown(user_input)

                # Generate chat history after adding user input
                chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state["messages"]])

                with st.spinner("Dattavism is typing..."):
                    response = answer_user_query(data=report,query=user_input,history=chat_history,data_set=df)
                    with st.chat_message('Dattavism',avatar="ai"):
                        response_container = st.empty()
                        streamed_response = ""

                        for chunk in response:
                            streamed_response += chunk
                            response_container.markdown(streamed_response)
                            time.sleep(0.01)

                    st.session_state["messages"].append({"role": "ai", "content": streamed_response})


        
