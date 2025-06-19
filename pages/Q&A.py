import time
import streamlit as st
from utils.gemini_ai import answer_user_query
from utils.visualizer import generate_visualizations
import pandas as pd
import matplotlib.pyplot as plt

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
    plot = st.session_state["plot"]
    Col1, Col2 = st.columns(2,border=False)
    with Col1:
        with st.expander("## Dataset Preview 🔍"):
            st.write(df.head(10))
        with st.expander("## Report Preview 📄"):
            with st.container(height=500):
                st.write(report)
        with st.expander("## Visualizations 📊"):
            with st.container(height=500):
                for i, chart in enumerate(plot):
                    chart_type = chart.get("chart_type")
                    x_column = chart.get("x_column")
                    y_column = chart.get("y_column")
                    reason = chart.get("reason")

                    st.subheader(f"{i+1}. {chart_type.capitalize()} Chart")
                    st.text(f"🧠 {reason}")

                    try: 
                        with st.container(border=True):
                            chart_df = pd.DataFrame(df)
                            if chart_type == "scatter":
                                fig, ax = plt.subplots(figsize=(3, 3))
                                ax.scatter(chart_df[y_column], chart_df[x_column])
                                ax.set_xlabel(x_column)
                                ax.set_ylabel(y_column)
                                st.pyplot(fig,use_container_width=True)
                            elif chart_type == "bar":
                                        fig, ax = plt.subplots(figsize=(9, 9))
                                        ax.bar(chart_df[x_column], chart_df[y_column])
                                        ax.set_xlabel(x_column)
                                        ax.set_ylabel(y_column)
                                        st.pyplot(fig,use_container_width=True)
                            elif chart_type == "line":
                                        st.line_chart(chart_df, x=x_column, y=y_column)
                            elif chart_type == "area":
                                        st.area_chart(chart_df, x=x_column, y=y_column)
                            elif chart_type == "pie":
                                        fig, ax = plt.subplots(figsize=(3, 3))
                                        ax.pie(chart_df[y_column], labels=chart_df[x_column], autopct='%1.1f%%', startangle=90)
                                        ax.axis('equal') # Equal aspect ratio ensures the pie chart is circular.
                                        st.pyplot(fig)
                            elif chart_type == "histogram":
                                        if y_column in chart_df.columns:

                                            st.pyplot(chart_df[y_column].plot.hist(bins=30, edgecolor='black'))
                                        else:
                                            st.error("Histogram requires a numerical column.")
                            elif chart_type == "map":
                                            if "latitude" in chart_df.columns and "longitude" in chart_df.columns:
                                                st.map(chart_df)
                                            else:
                                                st.error("Map visualization requires 'latitude' and 'longitude' columns.")
                            else:
                                        st.error(f"Unsupported chart type: {chart_type}")
                    except Exception as e:
                                    st.error(f"Could not render chart due to: {e}")

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
                    response = answer_user_query(data=report,query=user_input,history=chat_history,data_set=df,plots=plot)
                    with st.chat_message('Dattavism',avatar="ai"):
                        response_container = st.empty()
                        streamed_response = ""

                        for chunk in response:
                            streamed_response += chunk
                            response_container.markdown(streamed_response)
                            time.sleep(0.01)

                    st.session_state["messages"].append({"role": "ai", "content": streamed_response})


        
