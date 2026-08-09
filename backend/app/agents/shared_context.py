"""Defines the shared data structure passed between agents."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TicketContext(BaseModel):
    """Context related to a specific support ticket."""
    id: int
    subject: str
    description: str


class CustomerContext(BaseModel):
    """Context related to the customer."""
    id: int
    name: str
    email: str


class ToolCall(BaseModel):
    """Represents a decision to call a specific tool function."""
    tool_name: str
    function_name: str
    args: Dict[str, Any] = Field(default_factory=dict)


class SharedContext(BaseModel):
    """
    A shared data object that is passed between agents in a workflow.
    Each agent can read from and write to this object, enriching it with
    information as the workflow progresses.
    """
    # --- Input Fields ---
    user_query_audio: Optional[bytes] = None
    user_query_text: Optional[str] = None

    # --- Existing Ticket Ingestion Fields ---
    ticket: Optional[TicketContext] = None
    customer: Optional[CustomerContext] = None

    # --- Agent-Populated Fields ---
    language: Optional[str] = None
    classification: Optional[Dict[str, Any]] = None
    tool_call: Optional[ToolCall] = None
    tool_output: Optional[Any] = None
    suggested_response: Optional[str] = None
    internal_notes: List[str] = Field(default_factory=list)