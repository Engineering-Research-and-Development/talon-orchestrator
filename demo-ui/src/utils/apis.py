import json
import os
import requests

def get_metrics(algorithm="ts_linear_interpolation"):
    """
    Retrieve metrics for a given algorithm from an API.
    """
    url = "https://talon-curation-api.cluster1.alidalab.it/curation/choice"
    payload = {"input": algorithm}
    headers = {"content-type": "application/json", "accept": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        return json.loads(response.text)['optimization']['metrics']
    except requests.exceptions.RequestException as e:
        print("Error fetching metrics:", e)
        return None

def get_algorithms_per_task(task="interpolation"):
    """
    Retrieve available algorithms for a given task from an API.
    """
    url = "https://talon-curation-api.cluster1.alidalab.it/curation/choice"
    payload = {"input": task}
    headers = {"content-type": "application/json", "accept": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        return json.loads(response.text)['nextPossibleInputs']
    except requests.exceptions.RequestException as e:
        print("Error fetching algorithms:", e)
        return None

def columns_with_constant_value(df, constant=1):
    """
    Find columns in a DataFrame with a constant value.
    """
    constant_columns = [col for col in df.columns if (df[col] == constant).all()]
    return constant_columns

def get_non_null_columns(df):
    """
    Get columns in a DataFrame with non-null values.
    """
    non_null_columns = list(df.columns[df.notnull().any()])
    return non_null_columns

def get_tasks_list():
    """
    Retrieve a list of available tasks from an API.
    """
    url = "https://talon-curation-api.cluster1.alidalab.it/curation/choice"
    payload = {"input": "tabular"}
    headers = {"content-type": "application/json", "accept": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        return json.loads(response.text)['nextPossibleInputs']
    except requests.exceptions.RequestException as e:
        print("Error fetching tasks:", e)
        return None

# Example usage
# task = get_list_of_tasks()[2]
# algos = get_algorithms_per_task(task=task)
# metrics = get_metrics(algorithm=algos[0])
# common_metrics = columns_with_constant_value(df=df)
# sliders = get_non_null_columns(optimize_for_df.loc[common_metrics])
