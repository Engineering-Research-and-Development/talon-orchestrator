from datetime import datetime
import pandas as pd

def columns_with_constant_value(df: pd.DataFrame, constant=1):
    """
    Find columns in a DataFrame with a constant value.
    """
    return [col for col in df.columns if (df[col] == constant).all()]

def get_non_null_columns(df: pd.DataFrame):
    """
    Get columns in a DataFrame with non-null values.
    """
    return list(df.columns[df.notnull().any()])

def convert_to_title_case(snake_str):
    # Split the string by underscores
    words = snake_str.split('_')
    # Capitalize each word
    capitalized_words = [word.capitalize() for word in words]
    # Join the words with spaces
    title_case_str = ' '.join(capitalized_words)
    return title_case_str