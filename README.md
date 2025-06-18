


# 🔮 Dattavism (दत्ताविस्म)

Dattavism is an intelligent, AI-powered data insight platform built with Python, Streamlit, Gemini API, Pandas, Matplotlib, NumPy, and MySQL. It enables users from any domain—business, science, medical, social research—to upload a CSV dataset and receive a full, contextual report of patterns, visualizations, summaries, and insights without writing a single line of code.

### 🚀 What Dattavism can do 

- 📂 Accepts CSV data of any domain (business, science, healthcare, etc.)
- 🧠 Uses Gemini AI to understand the data context and generate meaningful narratives
- 📊 Automatically generates charts based on key patterns
- 📈 Allows custom visualizations with user-selected parameters
- 🤖 Supports Q&A—users can ask natural-language questions about the data
- 📄 Generates a downloadable insight report (PDF) including summaries, charts, and recommendations


# Quick Start Demo

###  🧪 How It Works

1. Upload your CSV file
2. Backend processes and understands your data
3. Gemini API generates textual descriptions and business insights
4. Visual charts and analytics are rendered dynamically
5. User can ask questions and customize visualizations
6. Export a downloadable PDF/Markdown report

# 🔑 Prerequisites
    Python 3.8+

    Google Gemini API Key

# 📦 Installation

```bash
git clone https://github.com/UnnatMalik/Dattavism-AI-Powered-Data-Insight-Generator-.git
cd Dattavism-AI-Powered-Data-Insight-Generator-

# Install dependencies
pip install -r requirements.txt

# Set Up Environment Variable
setx GEMINI_API_KEY "your_gemini_api_key"

# run streamlit app
streamlit run main.py

```

# ⚙️  Technologies



| Layer        | Tools/Technologies                  |
|--------------|-------------------------------------|
| Language   |  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge" height="40" alt="python logo"  />                                         |
| Frontend     | <img src="https://img.shields.io/badge/Streamlit-red?style=flat-square&logo=streamlit&logoColor=white" height="40" alt="Streamlit" />|
| AI Engine    | <img src="https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white" height="40" alt="Gemini" />                          |
| Data Engine  | <img src="https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white&style=for-the-badge" height="40" alt="pandas logo"  /> <img width="12" /> <img src="https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black" height="40" alt="Matplotlib" /> | 
| Reporting    | <img src="https://img.shields.io/badge/ReportLabs-gray?style=flat-square&logo=readthedocs" height="40" alt="ReportLabs" /> <img src="https://img.shields.io/badge/MarkDown-Blue?style=flat-square&logo=markdown&logoColor=Red" height="40" alt="MarkDown" />    |


# 🗺️ Roadmap
``` mermaid
flowchart TD
    A[User Uploads Data File] --> B[File Type Detection]
    B --> C{Supported Format?}
    C -->|Yes| D[Data Parsing & Preprocessing]
    C -->|No| E[Error: Unsupported Format]
    D --> F[Data Analysis & Statistical Profiling]
    F --> G[AI-Powered Insight Generation]
    G --> H[Visualization Selection]
    H --> I[Generate Interactive Charts]
    I --> J[Generate Natural Language Summary]
    J --> K[Display Insights Dashboard]
    K --> L[User Interacts with Results]
    L --> M{User Requests Export?}
    M -->|Yes| N[Export Insights as Report/Notebook]
    M -->|No| O[Session Ends]
    
    style A fill:#4CAF50,stroke:#388E3C
    style E fill:#FF5722,stroke:#E64A19
    style K fill:#2196F3,stroke:#1976D2
    style N fill:#9C27B0,stroke:#7B1FA2
```


