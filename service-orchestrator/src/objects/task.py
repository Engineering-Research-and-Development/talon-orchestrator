import os
import pandas as pd
import requests
import json
from services.task_service import TaskService 
from config import config
from utils.utils import get_non_null_columns, columns_with_constant_value

class Task:
    def __init__(self, selected_task):
        self.selected_task = selected_task
        self.file_name = "Models_tassonomy_metrics.csv"
        self.file_path = os.path.join(os.path.dirname(__file__), self.file_name)
        self.optimize_for_df = None
        self.algos = None
        self.df = None
        self.slider_descriptions = {
            "Better_results": "Prioritize accuracy, precision, lowers errors and losses.",
            "Faster_results": "Prioritize speed of execution.",
            "Greener_AI": "Prioritize energy consumption.",
            "Cost": "Prioritize cost reduction."
        }
        self.mapper = {
            "Better_results": "Quality",
            "Faster_results": "Speed",
            "Greener_AI": "Energy Efficiency",
            "Cost": "Cost"
        }
        self.sliders = []
        self.taskService = TaskService(base_url=config["TASK_URL"])

    def load_data(self):
        self.optimize_for_df = pd.read_csv(self.file_path, index_col="Metric")
        self.optimize_for_df = self.optimize_for_df[["Better_results", "Faster_results", "Greener_AI", "Cost"]]
        self.algos = self.taskService.get_algorithms_per_task(task=self.selected_task)

    def generate_metrics_table(self):
        self.df = pd.DataFrame(0, index=self.algos, columns=self.optimize_for_df.index)
        for algo in self.algos:
            metrics = self.taskService.get_metrics(algorithm=algo)
            for metric in metrics:
                if metrics[metric]['value'] is not None:
                    self.df.loc[algo, metric] = 1

    def filter_common_metrics_and_sliders(self):
        common_metrics = columns_with_constant_value(df=self.df)
        self.optimize_for_df = self.optimize_for_df.loc[common_metrics]
        self.sliders = get_non_null_columns(self.optimize_for_df)

    def get_slider_descriptions(self):
        return self.slider_descriptions

    def get_mapper(self):
        return self.mapper