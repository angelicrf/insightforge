"""A tool for interacting with the Salesforce API."""

import json
import os
from typing import Any, Dict

import httpx
import structlog

from app.config.settings import settings

log = structlog.get_logger()


class SalesforceTool:
    """A tool for agents to interact with Salesforce, using a cached token."""

    def __init__(self):
        self.access_token: str | None = None
        self.instance_url: str | None = None
        self._load_cached_token()

    def _load_cached_token(self):
        """Loads the access token and instance URL from the local cache file."""
        if os.path.exists(settings.SALESFORCE_TOKEN_FILE):
            try:
                with open(settings.SALESFORCE_TOKEN_FILE, "r") as f:
                    token_data = json.load(f)
                    self.access_token = token_data.get("access_token")
                    self.instance_url = token_data.get("instance_url")
                    if self.access_token and self.instance_url:
                        log.info("Salesforce client initialized with cached token.")
            except (IOError, json.JSONDecodeError) as e:
                log.error("Failed to load cached Salesforce token.", error=str(e))

    async def get_case_details(self, case_id: str) -> Dict[str, Any]:
        """Retrieves details for a specific Salesforce Case using the cached token."""
        if not self.access_token or not self.instance_url:
            log.warning("Salesforce token not available. Returning mock data.")
            return {"Id": case_id, "Subject": "Mock Case (No Token)", "Status": "New"}

        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.instance_url}/services/data/v59.0/sobjects/Case/{case_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        return response.json()

    async def query_pardot_custom_fields(self) -> Dict[str, Any]:
        """Queries the Pardot API for custom fields."""
        if not self.access_token:
            log.warning("Salesforce/Pardot token not available. Cannot query custom fields.")
            raise httpx.HTTPStatusError(
                "Pardot token not available. Please authenticate with Salesforce first.",
                request=None,
                response=httpx.Response(401),
            )

        if not settings.PARDOT_BUSINESS_UNIT_ID:
            log.warning("PARDOT_BUSINESS_UNIT_ID is not configured.")
            raise ValueError("PARDOT_BUSINESS_UNIT_ID is not configured in settings.")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Pardot-Business-Unit-Id": settings.PARDOT_BUSINESS_UNIT_ID,
        }
        # The Pardot API host is different from the main Salesforce instance URL.
        url = "https://pi.pardot.com/api/customField/version/4/do/query?format=json"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
