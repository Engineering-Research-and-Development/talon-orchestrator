import requests
import json
import logging
from config import config

class PodService:
    def __init__(self):
        self.url = config["K8S_API_URL"]
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic YWxpZGE6YWxpZGFncm91cA=='
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_pod_name_and_status(self):
        payload = json.dumps({"label": "someLabel=test1"})
        try:
            response = requests.get(self.url, headers=self.headers, data=payload)
            response.raise_for_status()
            pod_info = response.json()
            if pod_info:
                return pod_info[0][0], pod_info[0][1]
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error retrieving pod status: {e}")
            return None, None

    def get_status_icon_and_color(self, status):
        status_map = {
            "Running": ("check_circle", "yellow"),
            "Pending": ("hourglass_empty", "orange"),
            "Failed": ("cancel", "red"),
            "Succeeded": ("check_circle", "green"),
            "Unknown": ("help", "gray")
        }
        return status_map.get(status, ("help", "gray"))
