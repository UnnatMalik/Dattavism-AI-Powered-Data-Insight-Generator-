import streamlit as st 
from utils.gemini_ai import generate_report, answer_user_query, context_detection 
from utils.visualizer import generate_visualizations
from utils.pdf_generator import EnhancedReportGenerator
# ...existing code...
import pandas as pd
import os
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="AI Insight Report",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

class Pages_switch():
    st.sidebar.page_link("main.py", label="Home 🏠")
    st.sidebar.page_link("pages/upload_data.py", label="Upload Data-Sets 📂")
    st.sidebar.page_link("pages/report.py", label="Data-Set report 📄")

st.title("📊 AI-Powered Data Insight Report")
st.markdown("---")

if "df" in st.session_state:
    df = st.session_state["df"]
    context = context_detection(df)
    report = generate_report(df)
    plot = generate_visualizations(df)
    st.session_state["plot"] = plot
    st.session_state["report"] = report
    st.session_state["context"] = context
    if context and report: 
        st.subheader("Context Detection")
        st.write(context)
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Data-set overview","📄 AI Generated Report ","🤖 AI Suggested Charts","Custom Charts 📈","Download Report 📩"])

        with tab1:
            st.header("Data-set Overview 🔍")
            st.write("### Data Summary:")
            st.write(df.describe())
            st.write("### Sample Data:")
            st.dataframe(df.head(10))


        with tab2:
            st.write(report)
            
        
        with tab3:
           st.header("AI Generated Visualizations 📊")
           if "plot" in st.session_state:
                for i,chart in enumerate(st.session_state["plot"]):
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
        with tab5:
            st.header("Download Report 📩")
            if st.button("Generate Complete Report"):
                with st.spinner("Creating PDF report..."):
                    report_generator = EnhancedReportGenerator()
                    success = report_generator.create_complete_report(
                            context_response=st.session_state["context"],
                            report_response=st.session_state["report"],
                            df=df,   
                            figures=st.session_state["plot"],
                            output_path="analysis_report.pdf",
                            report_title=f"Analysis report on {st.session_state["filename"]}"
                        )
                    if success:
                        # Read the generated PDF file
                        with open("analysis_report.pdf", "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                        
                        # Create download button
                        # Ensure the reports directory exists
                        reports_dir = "report"
                        os.makedirs(reports_dir, exist_ok=True)
                        report_path = os.path.join(reports_dir, "analysis_report.pdf")

                        # Save the PDF file to the reports folder
                        with open(report_path, "wb") as f:
                            f.write(pdf_bytes)

                        # Create download button for the file in the reports folder
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_bytes,
                            file_name="analysis_report.pdf",
                            mime="application/pdf"
                        )
                        st.success("Report generated successfully! Click the download button above to get your PDF.")
                    else:
                        st.error("Failed to generate the report. Please try again.")
        with tab4:
            st.header("Custom Charts 📈")
            st.write("You can create custom charts based on the dataset.")
            Column_data = pd.DataFrame(df)
            
            # Show sample of the data
            st.write("Sample of your data:")
            st.write(Column_data.head())
            
            # Chart selection and configuration
            chart_type = st.selectbox("Select Chart Type", ["Bar", "Line", "Scatter", "Pie", "Histogram", "Heatmap"])
            y_columns = st.selectbox("Select Y Column", Column_data.columns) if chart_type != "Heatmap" else None
            x_columns = st.selectbox("Select X Column", Column_data.columns) if chart_type not in ["Pie", "Histogram", "Heatmap"]else None
            
            if st.button("Generate Custom Chart"):
                try:
                    if chart_type == "Scatter":
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.scatter(Column_data[x_columns], Column_data[y_columns])
                        ax.set_xlabel(x_columns)
                        ax.set_ylabel(y_columns)
                        st.pyplot(fig, use_container_width=True)
                    
                    elif chart_type == "Bar":
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.bar(Column_data[x_columns], Column_data[y_columns])
                        ax.set_xlabel(x_columns)
                        ax.set_ylabel(y_columns)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig, use_container_width=True)
                    
                    elif chart_type == "Line":
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.plot(Column_data[x_columns], Column_data[y_columns])
                        ax.set_xlabel(x_columns)
                        ax.set_ylabel(y_columns)
                        plt.tight_layout()
                        st.pyplot(fig, use_container_width=True)
                    
                    elif chart_type == "Pie":
                        fig, ax = plt.subplots(figsize=(10, 6))
                        # Group data for pie chart
                        pie_data = Column_data[y_columns].value_counts()
                        ax.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%')
                        ax.axis('equal')
                        plt.title(f"Distribution of {y_columns}")
                        st.pyplot(fig, use_container_width=True)
                    
                    elif chart_type == "Histogram":
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.hist(Column_data[y_columns], bins=30, edgecolor='black')
                        ax.set_xlabel(y_columns)
                        ax.set_ylabel('Frequency')
                        plt.tight_layout()
                        st.pyplot(fig, use_container_width=True)
                    
                    elif chart_type == "Heatmap":
                        fig, ax = plt.subplots(figsize=(12, 8))
                        correlation_matrix = Column_data.corr()
                        im = ax.imshow(correlation_matrix, cmap='coolwarm')
                        
                        # Add colorbar
                        plt.colorbar(im, label='Correlation Coefficient')
                        
                        # Add labels
                        ax.set_xticks(range(len(correlation_matrix.columns)))
                        ax.set_yticks(range(len(correlation_matrix.columns)))
                        ax.set_xticklabels(correlation_matrix.columns, rotation=45, ha='right')
                        ax.set_yticklabels(correlation_matrix.columns)
                        
                        # Add correlation values
                        for i in range(len(correlation_matrix.columns)):
                            for j in range(len(correlation_matrix.columns)):
                                text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                                             ha='center', va='center', 
                                             color='white' if abs(correlation_matrix.iloc[i, j]) > 0.5 else 'black')
                        
                        plt.title("Correlation Heatmap")
                        plt.tight_layout()
                        st.pyplot(fig, use_container_width=True)

                        
                except Exception as e:
                    st.error(f"Could not render custom chart due to: {e}")
                    st.write("Please make sure you've selected appropriate columns for the chart type.")

                     
else:
    st.warning("Please upload a CSV file to generate insights and visualizations.")
    st.markdown("Upload a CSV file from the **Upload Data-Sets** page to get started.")
st.markdown("---")    