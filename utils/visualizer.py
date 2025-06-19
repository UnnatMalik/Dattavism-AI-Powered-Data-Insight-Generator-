import json
import re
import google.generativeai as genai 
import pandas as pd 
import os
# Configure Gemini AI with API key from environment variables
genai.configure(
    api_key=os.getenv("GEMINI_API")
)

# Initialize model with visualization-specific instructions
model = genai.GenerativeModel("gemini-2.0-flash", system_instruction="You are a data analysis assistant. You will help users visualize their datasets.")

def detect_format(df):
    """
    Detects if the DataFrame is in wide format based on column characteristics.
    
    Args:
        df (pandas.DataFrame): Input DataFrame to analyze
        
    Returns:
        str or None: Returns 'Wide' if the DataFrame is in wide format, None otherwise
        
    Notes:
        - Checks for unique values in columns
        - Identifies potential ID columns
        - Looks for year-like columns (starting with 19xx or 20xx)
        
    Example:
        >>> data = pd.read_csv('sales_by_year.csv')
        >>> format_type = detect_format(data)
        >>> print(format_type)
        'Wide'
    """
    num_unique_cols = df.nunique()
    likely_id_cols = num_unique_cols[num_unique_cols > 1].index.tolist()

    wide_likelihood = any(
        col.strip().isdigit() or str(col).lower().startswith(("20", "19"))
        for col in df.columns
    )
    if wide_likelihood:
        return "Wide"


def generate_visualizations(data):
    """
    Generates visualization recommendations based on dataset characteristics.
    
    Args:
        data (pandas.DataFrame): Dataset to analyze for visualization opportunities
        
    Returns:
        list: List of dictionaries containing visualization recommendations:
            - chart_type: Type of chart (bar, line, scatter, etc.)
            - x_column: Column to use for x-axis
            - y_column: Column to use for y-axis (if applicable)
            - reason: Explanation of the insight this visualization would reveal
            
    Chart Types:
        - Bar charts: For categorical comparisons
        - Line charts: For time-based trends
        - Scatter plots: For correlations
        - Pie charts: For proportional data
        - Histograms: For distribution analysis
        - Maps: For geographical data
        
    Example:
        >>> df = pd.read_csv('sales_data.csv')
        >>> viz_recommendations = generate_visualizations(df)
        >>> print(viz_recommendations)
        [
            {
                "chart_type": "bar",
                "x_column": "category",
                "y_column": "sales",
                "reason": "Shows sales distribution across categories"
            },
            ...
        ]
    
    Notes:
        - Handles both wide and long format data
        - Automatically reshapes wide format data using pd.melt()
        - Returns empty list if JSON parsing fails
        - Uses Gemini AI for intelligent chart recommendations
    """
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

        
    
