"""
Dynatrace Client

Low-level client for calling Dynatrace APIs.

This module should only know how to talk to Dynatrace.
It should not contain assurance logic.
"""

import os

import requests
from dotenv import load_dotenv


load_dotenv()


class DynatraceClient:
    """Simple Dynatrace API client."""

    def __init__(self):
        self.base_url = os.getenv("DYNATRACE_URL", "").rstrip("/")
        self.api_token = os.getenv("DYNATRACE_API_TOKEN", "")

        if not self.base_url:
            raise ValueError("DYNATRACE_URL is not set.")

        if not self.api_token:
            raise ValueError("DYNATRACE_API_TOKEN is not set.")

        self.headers = {
            "Authorization": f"Api-Token {self.api_token}",
            "Accept": "application/json",
        }

    def get_entities(self, entity_selector: str, page_size: int = 100) -> dict:
        """Fetch Dynatrace entities matching an entity selector."""

        url = f"{self.base_url}/api/v2/entities"

        params = {
            "entitySelector": entity_selector,
            "pageSize": page_size,
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_metrics(self, metric_selector: str, page_size: int = 100) -> dict:
        """Fetch Dynatrace metric descriptors."""

        url = f"{self.base_url}/api/v2/metrics"

        params = {
            "metricSelector": metric_selector,
            "pageSize": page_size,
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def query_metric_data(
        self,
        metric_selector: str,
        entity_selector: str | None = None,
        from_time: str = "now-30m",
        to_time: str = "now",
        resolution: str = "Inf",
    ) -> dict:
        """Query metric data from Dynatrace."""

        url = f"{self.base_url}/api/v2/metrics/query"

        params = {
            "metricSelector": metric_selector,
            "from": from_time,
            "to": to_time,
            "resolution": resolution,
        }

        if entity_selector:
            params["entitySelector"] = entity_selector

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_problems(self, page_size: int = 100) -> dict:
        """Fetch open Dynatrace problems."""

        url = f"{self.base_url}/api/v2/problems"

        params = {
            "pageSize": page_size,
            "problemSelector": 'status("open")',
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()
