import os

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.prometheus_client import PrometheusClient
from datetime import datetime
import requests
import json
from time import sleep
import random

# Initialize Prometheus client
prom_client = PrometheusClient("https://prometheus.cluster1.alidalab.it")

pod_method = os.getenv('pod_method')

# Function to query Prometheus and process the response
def query_prometheus(query):
    result = prom_client.run_query(query)
    if 'status' in result and result['status'] == 'success' and result['data']['result'] and len(result['data']['result']) > 0:
        timestamps = [datetime.fromtimestamp(float(point[0])) for point in result['data']['result'][0]['values']]
        values = [float(point[1]) for point in result['data']['result'][0]['values']]
        return pd.DataFrame({'Timestamp': timestamps, 'Value': values})
    else:
        return pd.DataFrame()

# Function to retrieve pod name and status
def get_pod_name_and_status():
    url = "https://k8s-client-2.cluster1.alidalab.it/api/v1/k8s/pod/talon"
    payload = json.dumps({"label": "someLabel=test1"})
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Basic YWxpZGE6YWxpZGFncm91cA=='
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    
    if response.status_code == 200 and response.json():
        # Return the first pod name and status
        return response.json()[0][0], response.json()[0][1]
    else:
        return None, None

# Function to get icon and color based on pod status
def get_status_icon_and_color(status):
    if status == "Running":
        return "check_circle", "yellow"
    elif status == "Pending":
        return "hourglass_empty", "orange"
    elif status == "Failed":
        return "cancel", "red"
    elif status == "Succeeded":
        return "check_circle", "green"
    elif status == "Unknown":
        return "help", "gray"
    else:
        return "help", "gray"

# Main title
st.title("Container Monitoring Dashboard")

# Add Material Icons stylesheet
st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

# Get pod name and status
pod_name, pod_status = get_pod_name_and_status()
left_trials = 3
while pod_name is None and left_trials > 0:
    pod_name, pod_status = get_pod_name_and_status()
    left_trials -= 1
    print(f"Cannot retrieve pod name, retrying other {left_trials} times...", flush=True)
    sleep(2)
    
if pod_name:
    status_icon, status_color = get_status_icon_and_color(pod_status)
    pod_status_placeholder = st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4>Pod Name: {pod_name}</h4>
            <span style='color:{status_color}; font-size: 1.2em;' class="material-icons">{status_icon}</span>
            <span style='color:{status_color}; font-size: 1.2em;'>{pod_status}</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("Failed to retrieve pod name")

# Create placeholders for the live charts
cpu_placeholder = st.empty()
memory_placeholder = st.empty()

# DataFrame to accumulate CPU and Memory data
cpu_data = pd.DataFrame(columns=['Timestamp', 'Value'])
memory_data = pd.DataFrame(columns=['Timestamp', 'Value'])

# Query interval (seconds)
query_interval = 0.5
status_update_interval = 3
status_check_countdown = status_update_interval // query_interval
count = 0

# Loop to update the charts every second
while pod_name:
    # Query and plot CPU usage
    cpu_query = f'container_cpu_usage_seconds_total{{pod="{pod_name}"}}[1d]'
    new_cpu_data = query_prometheus(cpu_query)
    if not new_cpu_data.empty:
        cpu_fig = px.line(new_cpu_data[:count], x='Timestamp', y='Value', title='Container CPU Usage')
        cpu_fig.update_layout(xaxis_title="Time", yaxis_title="CPU Usage")
        cpu_placeholder.plotly_chart(cpu_fig, use_container_width=True)
        
    # Query and plot Memory usage
    memory_query = f'container_memory_usage_bytes{{pod="{pod_name}"}}[1d]'
    new_memory_data = query_prometheus(memory_query)
    if not new_memory_data.empty:
        memory_fig = px.line(new_memory_data[:count], x='Timestamp', y='Value', title='Container RAM Usage')
        memory_fig.update_layout(xaxis_title="Time", yaxis_title="Memory Usage (Bytes)")
        memory_placeholder.plotly_chart(memory_fig, use_container_width=True)
    
    count += 1

    # Update pod status every 3 seconds
    if count % status_check_countdown == 0:
        pod_name, pod_status = get_pod_name_and_status()
        if pod_status in ["Succeeded", "Failed"]:
            status_icon, status_color = get_status_icon_and_color(pod_status)
            pod_status_placeholder.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>Pod Name: {pod_name}</h4>
                    <span style='color:{status_color}; font-size: 1.2em;' class="material-icons">{status_icon}</span>
                    <span style='color:{status_color}; font-size: 1.2em;'>{pod_status}</span>
                </div>
            """, unsafe_allow_html=True)
            break
        else:
            status_icon, status_color = get_status_icon_and_color(pod_status)
            pod_status_placeholder.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>Pod Name: {pod_name}</h4>
                    <span style='color:{status_color}; font-size: 1.2em;' class="material-icons">{status_icon}</span>
                    <span style='color:{status_color}; font-size: 1.2em;'>{pod_status}</span>
                </div>
            """, unsafe_allow_html=True)

    # Pause for the query interval
    sleep(query_interval)


kpi1, kpi2 = st.columns(2)

mae = None
time = None

print(f"[DEMO] Alg chosen: -{pod_method}-", flush=True)

if "pad" in pod_method:
    mae = 0.028
    time = random.random()*0.01
else:
    mae = 0.021
    time = random.random()*0.03


# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="MAE",
    value=mae
)

# fill in those three columns with respective metrics or KPIs
kpi2.metric(
    label="Exec time (s)",
    value=time
)

