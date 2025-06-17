import json
import re
import google.generativeai as genai 
import pandas as pd 
import os
genai.configure(
    api_key=os.getenv("API_KEY")
)

model = genai.GenerativeModel("gemini-2.0-flash", system_instruction="You are a data analysis assistant. You will help users visiualize their datasets .")

def detect_format(df):
    num_unique_cols = df.nunique()
    likely_id_cols = num_unique_cols[num_unique_cols > 1].index.tolist()

    wide_likelihood = any(
        col.strip().isdigit() or str(col).lower().startswith(("20", "19"))
        for col in df.columns
    )
    if wide_likelihood:
        return "Wide"


def generate_visualizations(data):
    content = pd.DataFrame(data)
    if detect_format(content) == "Wide":
        content = pd.melt(content)
        prompt = f"""
        You are a data analyst. Based on the following dataframe (summarized):

        {content}

        Suggest 2-3 useful visualizations to explore this data.
        For each suggestion, include:
        - chart_type (e.g., bar, pie, line, scatter)
        - x_column
        - y_column (if applicable)
        - Explain briefly what insight each visualization would reveal
        - Recommend Charts Based on Patterns:
            - Bar charts for categorical comparisons
            - Line charts for time-based trends
            - Scatter plots for correlations
            - Pie/donut charts for proportions
            - Histograms for distribution
            - Map visualizations for geographical data
        

        Respond in **pure JSON** like:
        [
        {{
            "chart_type": "bar",
            "x_column": "category",
            "y_column": "sales",
            "reason": "Shows sales per category."
        }},
        ...
        ]
        """
        model_response = model.generate_content(
            contents=prompt 
        )
        try:
            json_block = re.search(r"\[\s*{.*}\s*\]", model_response.text.strip(), re.DOTALL)
            if json_block:
                return json.loads(json_block.group())
            else:
                return []
        except json.JSONDecodeError as e:
            print("JSON Error:", e)
            return []
    else:
        prompt = f"""
    You are a data analyst. Based on the following dataframe (summarized):

    {content}

    Suggest 2-3 useful visualizations to explore this data.
    For each suggestion, include:
    - chart_type (e.g., bar, pie, line, scatter)
    - x_column
    - y_column (if applicable)
    - Explain briefly what insight each visualization would reveal
    - Recommend Charts Based on Patterns:
        - Bar charts for categorical comparisons
        - Line charts for time-based trends
        - Scatter plots for correlations
        - Pie charts for proportions
        - Histograms for distribution
        - Map visualizations for geographical data
    - Only suggest charts that are useful and relevant based on the structure and semantics of the data.
      Avoid meaningless or redundant suggestions.
    

    Respond in **pure JSON** like:
    [
      {{
        "chart_type": "bar",
        "x_column": "category",
        "y_column": "sales",
        "reason": "Shows sales per category."
      }},
      ...
    ]

    """
    model_response = model.generate_content(
        contents=prompt 
    )
    try:
        json_block = re.search(r"\[\s*{.*}\s*\]", model_response.text.strip(), re.DOTALL)
        if json_block:
            return json.loads(json_block.group())
        else:
            return []
    except json.JSONDecodeError as e:
        print("JSON Error:", e)
        return []

        
    
