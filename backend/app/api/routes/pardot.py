"""API endpoints for interacting with Salesforce Pardot."""

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from httpx import HTTPStatusError

from app.tools.salesforce_client import SalesforceTool

router = APIRouter()

# Instantiate the tool. In a larger app, this might be a dependency.
salesforce_tool = SalesforceTool()


@router.get("/custom-fields", response_model=Dict[str, Any])
async def get_pardot_custom_fields():
    """Retrieves custom fields from the Pardot API."""
    try:
        return await salesforce_tool.query_pardot_custom_fields()
    except (HTTPStatusError, ValueError) as e:
        status_code = e.response.status_code if isinstance(e, HTTPStatusError) else 400
        detail = str(e)
        raise HTTPException(status_code=status_code, detail=detail)