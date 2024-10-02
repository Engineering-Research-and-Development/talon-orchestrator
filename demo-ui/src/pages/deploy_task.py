import streamlit as st
from streamlit import switch_page
import streamlit_vertical_slider as svs
import json
import requests
import pandas as pd
import numpy as np
import os
from utils.apis import get_algorithms_per_task, get_metrics, columns_with_constant_value, get_non_null_columns
from utils.string_utils import convert_to_title_case
import json
st.set_page_config(page_title="Model Deploy", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

slider_values = {}
slider_descriptions = {
    "Better_results": "Prioritize accuracy, precision, lowers errors and losses.",
    "Faster_results": "Prioritize speed of execution.",
    "Greener_AI": "Prioritize energy consumption.",
    "Cost": "Prioritize cost reduction."
}

mapper = {
    "Better_results": "Quality",
    "Faster_results": "Speed",
    "Greener_AI": "Energy Efficiency",
    "Cost": "Cost"
}

# Load data
task = os.environ.get("selected_task")
file_name = "Models_tassonomy_metrics.csv"
file_path = os.path.join(os.path.dirname(__file__), file_name)
optimize_for_df = pd.read_csv(file_path, index_col="Metric")
optimize_for_df = optimize_for_df[["Better_results", "Faster_results", "Greener_AI", "Cost"]]
algos = get_algorithms_per_task(task=task)

# Generate metrics/algo table
df = pd.DataFrame(0, index=algos, columns=optimize_for_df.index)
for algo in algos:
    metrics = get_metrics(algorithm=algo)
    for metric in metrics:
        if metrics[metric]['value'] is not None:
            df.loc[algo, metric] = 1
        

# Filter common metrics and sliders
common_metrics = columns_with_constant_value(df=df)
optimize_for_df = optimize_for_df.loc[common_metrics]
sliders = get_non_null_columns(optimize_for_df)


st.title("Task Optimization")


# UI
n_of_sliders = len(sliders)
bottom_cols = st.columns(n_of_sliders)

col_index = 0
for metric in sliders:
    with bottom_cols[col_index]:

        st.subheader(mapper[metric])
        slider_values[metric] = svs.vertical_slider(
            label=slider_descriptions[metric],
            default_value=50,
            step=1,
            min_value=0,
            max_value=100,
            key=str(metric),
            slider_color="orange",
            thumb_color="red",
            track_color="gray",
            value_always_visible=True
        )
    col_index+=1
   
# Center the "Deploy Model" button with 25% width using HTML and CSS
st.markdown(
    """
    <style>
    .deploy-btn-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .deploy-btn {
        width: 25vw;
    }
    </style>
    <div class="deploy-btn-container">
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
if col2.button("Deploy Model", use_container_width=True):
    st.text("Deploying...")  # Provide feedback
    url = "https://k8s-client-2.cluster1.alidalab.it/api/v1/orchestrator/deploy/talon/interpolation-pod"
    payload = {
      "task": "Time series interpolation",
      "parameters": {
        "Quality": slider_values["Better_results"],
        "Speed of execution": slider_values["Faster_results"],
        "Energy efficiency": slider_values["Greener_AI"],
        "Cost reduction": slider_values["Cost"]
      }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWxpZGE6YWxpZGFncm91cA=='
    }
    
    
    text_for_log = {"parameters": {
        "Quality": slider_values["Better_results"],
        "Speed of execution": slider_values["Faster_results"],
        "Energy efficiency": slider_values["Greener_AI"],
        "Cost reduction": slider_values["Cost"]
      }}
    print(f"[DEMO] Deploying model with following values: \n {text_for_log}", flush=True)
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = json.loads(response.text)

        if 'labels' in data and 'method' in data['labels']:
            os.environ["pod_method"] = data['labels']['method']
        
        pod_name = data["labels"]["app"]
        print(f"[DEMO] Deployed Pod ({pod_name})", flush=True)
        st.text("Deployment successful!")
        switch_page("pages/monitor_task.py")
    else:
        st.text(f"Deployment failed. Error: {response.text}")
            
        
st.markdown("</div>", unsafe_allow_html=True)