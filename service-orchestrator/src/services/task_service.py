import requests
from config import config
import os 
import json 
from utils.utils import *

class TaskService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"content-type": "application/json", "accept": "application/json"}

    def post(self, payload):
        """
        Make a POST request to the API.
        """
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()  # Return the JSON content as a dict
        except requests.exceptions.RequestException as e:
            print(f"Error making POST request: {e}")
            return None

    def get_tasks_list(self):
        """
        Retrieve a list of available tasks from the API.
        """
        payload = {"input": "tabular"}
        result = self.post(payload)
        return result.get('nextPossibleInputs', []) if result else None

    def get_algorithms_per_task(self, task="interpolation"):
        """
        Retrieve available algorithms for a given task from the API.
        """
        payload = {"input": task}
        result = self.post(payload)
        return result.get('nextPossibleInputs', []) if result else None

    def get_metrics(self, algorithm="ts_linear_interpolation"):
        """
        Retrieve metrics for a given algorithm from the API.
        """
        payload = {"input": algorithm}
        result = self.post(payload)
        return result.get('optimization', {}).get('metrics', []) if result else None
    
    def prepare_deploy_data(self):
        
        task = os.environ.get("selected_task")
        
        if not task:
            return None, None, None, None

        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Models_tassonomy_metrics.csv')
        optimize_for_df = pd.read_csv(file_path, index_col="Metric")
        optimize_for_df = optimize_for_df[["Better_results", "Faster_results", "Greener_AI", "Cost"]]
        
        algos = self.get_algorithms_per_task(task=task)

        # Generate metrics/algo table
        df = pd.DataFrame(0, index=algos, columns=optimize_for_df.index)
        for algo in algos:
            metrics = self.get_metrics(algorithm=algo)
            for metric in metrics:
                if metrics[metric]['value'] is not None:
                    df.loc[algo, metric] = 1

        # Filter common metrics and sliders
        common_metrics = columns_with_constant_value(df=df)
        optimize_for_df = optimize_for_df.loc[common_metrics]
        sliders = get_non_null_columns(optimize_for_df)

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

        return task, sliders, slider_descriptions, mapper

    def deploy_model(self, task, slider_values):
        payload = {
            "task": task,
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

        url = "https://k8s-client-2.cluster1.alidalab.it/api/v1/orchestrator/deploy/talon/interpolation-pod"

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = json.loads(response.text)
            pod_name = data["labels"]["app"]
            return True, pod_name
        else:
            return False, response.text