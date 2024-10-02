from objects.prometheus import Prometheus
from config import config
import datetime
import pandas as pd

class PrometheusService:
    def __init__(self):
        self.client = Prometheus(config["PROMETHEUS_BASE_URL"])
    
    def process_prometheus_result(result):
        if result and len(result) > 0:
            timestamps = [datetime.fromtimestamp(float(point[0])) for point in result[0]['values']]
            values = [float(point[1]) for point in result[0]['values']]
            return pd.DataFrame({'Timestamp': timestamps, 'Value': values})
        return pd.DataFrame()
    
    def get_cpu_usage(self, pod_name):
        query = f'container_cpu_usage_seconds_total{{pod="{pod_name}"}}[1d]'
        result = self.client.run_query(query)
        return self.process_prometheus_result(result)

    def get_memory_usage(self, pod_name):
        query = f'container_memory_usage_bytes{{pod="{pod_name}"}}[1d]'
        result = self.client.run_query(query)
        return self.process_prometheus_result(result)
