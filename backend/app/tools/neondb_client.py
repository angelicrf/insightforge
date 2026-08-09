"""A tool for interacting with the NeonDB API."""

from typing import Any, Dict, List

import httpx
import structlog

from app.config.settings import settings

log = structlog.get_logger()


class NeonDBTool:
    """
    A tool for agents to inspect the Neon database by calling the internal API.

    Note: This requires the server to be running and accessible. It also needs
    a way to authenticate as an admin to use the protected /neoondb routes.
    For development, this might involve passing a dev-only admin token.
    """

    def __init__(self, internal_api_base_url: str, admin_token: str):
        self.base_url = internal_api_base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {admin_token}"}
        log.info("NeonDB client initialized for internal API calls.")

    async def list_tables(self) -> List[str]:
        """Retrieves a list of all table names in the public schema."""
        url = f"{self.base_url}/api/v1/neoondb/tables"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json().get("tables", [])
            except httpx.HTTPStatusError as e:
                log.error("Failed to list NeonDB tables.", error=str(e), response=e.response.text)
                return [f"Error: {e.response.status_code} - {e.response.text}"]

    async def get_table_data(self, table_name: str) -> Dict[str, Any]:
        """Fetches all rows from a specific table."""
        url = f"{self.base_url}/api/v1/neoondb/tables/{table_name}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                log.error("Failed to get table data.", table=table_name, error=str(e), response=e.response.text)
                return {"error": f"Error: {e.response.status_code} - {e.response.text}"}