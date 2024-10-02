from flask import render_template
from app import app

from services.pod_service import PodService
from services.prometheus_service import PrometheusService
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.io as pio
import random
import os

from config import config
import logging

# create logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s',
                    handlers=[logging.StreamHandler(), 
                              logging.FileHandler('app.log', mode='a')])

logger = logging.getLogger(__name__)

# base route
base_route = '/api/v1/'

 # Initialize services
pod_service = PodService()
prom_service = PrometheusService()

@app.route('/monitor')
def monitor():
    pod_name, pod_status = pod_service.get_pod_name_and_status()
    
    # Retry logic if pod name is not retrieved
    retry_attempts = 3
    while not pod_name and retry_attempts > 0:
        pod_name, pod_status = pod_service.get_pod_name_and_status()
        retry_attempts -= 1
        sleep(2)
    
    if pod_name:
        status_icon, status_color = pod_service.get_status_icon_and_color(pod_status)

        # Generate charts
        cpu_data = prom_service.get_cpu_usage(pod_name)
        memory_data = prom_service.get_memory_usage(pod_name)
        
        if not cpu_data.empty:
            cpu_fig = px.line(cpu_data, x='Timestamp', y='Value', title='Container CPU Usage')
            cpu_fig.update_layout(xaxis_title="Time", yaxis_title="CPU Usage")
            cpu_chart = pio.to_html(cpu_fig, full_html=False)
        else:
            cpu_chart = "<p>No data available</p>"

        if not memory_data.empty:
            memory_fig = px.line(memory_data, x='Timestamp', y='Value', title='Container RAM Usage')
            memory_fig.update_layout(xaxis_title="Time", yaxis_title="Memory Usage (Bytes)")
            memory_chart = pio.to_html(memory_fig, full_html=False)
        else:
            memory_chart = "<p>No data available</p>"
        
        # KPIs
        pod_method = os.getenv('pod_method', 'default_method')
        mae, exec_time = None, None
        
        if "pad" in pod_method:
            mae = 0.028
            exec_time = random.random() * 0.01
        else:
            mae = 0.021
            exec_time = random.random() * 0.03
        
        return render_template('monitor.html',
                               pod_name=pod_name,
                               pod_status=pod_status,
                               status_icon=status_icon,
                               status_color=status_color,
                               cpu_chart=cpu_chart,
                               memory_chart=memory_chart,
                               mae=mae,
                               exec_time=exec_time)
    else:
        return "<h1>Failed to retrieve pod name</h1>"