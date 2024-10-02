import requests
import logging
from datetime import datetime
from requests.exceptions import RequestException

class Prometheus:
    def __init__(self, base_url, timeout=10):
        """
        Initialize the Prometheus client.
        
        :param base_url: The base URL of the Prometheus server.
        :param timeout: The timeout for HTTP requests in seconds.
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def run_query(self, query, time=None):
        """
        Run a Prometheus query.

        :param query: The Prometheus query to run.
        :param time: The evaluation time for the query (optional).
        :return: The query result as a Python dictionary.
        :raises: ValueError if the query or response is invalid.
        """
        url = f"{self.base_url}/api/v1/query"
        params = {'query': query}
        if time:
            params['time'] = self._format_time(time)

        try:
            with requests.Session() as session:
                self.logger.info(f"Running query: {query}")
                response = session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                result = response.json()
                if result.get('status') != 'success':
                    raise ValueError(f"Query failed with status: {result.get('status')}")
                return result['data']['result']
        except (RequestException, ValueError) as e:
            self.logger.error(f"Error running query: {e}")
            raise

    def run_range_query(self, query, start, end, step):
        """
        Run a Prometheus range query.

        :param query: The Prometheus query to run.
        :param start: The start time for the range query (datetime or str).
        :param end: The end time for the range query (datetime or str).
        :param step: The step duration for the range query (e.g., '15s').
        :return: The query result as a Python dictionary.
        :raises: ValueError if the query or response is invalid.
        """
        url = f"{self.base_url}/api/v1/query_range"
        params = {
            'query': query,
            'start': self._format_time(start),
            'end': self._format_time(end),
            'step': step
        }

        try:
            with requests.Session() as session:
                self.logger.info(f"Running range query: {query} from {start} to {end} with step {step}")
                response = session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                result = response.json()
                if result.get('status') != 'success':
                    raise ValueError(f"Range query failed with status: {result.get('status')}")
                return result['data']['result']
        except (RequestException, ValueError) as e:
            self.logger.error(f"Error running range query: {e}")
            raise

    def _format_time(self, dt):
        """
        Format a datetime object or string to a string in the format expected by Prometheus.

        :param dt: The datetime object or string to format.
        :return: A string representing the formatted datetime.
        :raises: ValueError if the datetime is not properly formatted.
        """
        if isinstance(dt, datetime):
            return dt.isoformat()
        elif isinstance(dt, str):
            # Validate datetime string format
            try:
                datetime.fromisoformat(dt)
                return dt
            except ValueError:
                raise ValueError(f"Invalid datetime format: {dt}")
        else:
            raise ValueError(f"Invalid type for time formatting: {type(dt)}")
