"""Defines the shared data structure passed between agents."""

from typing import Any

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
    args: dict[str, Any] = Field(default_factory=dict)


class SharedContext(BaseModel):
    """
    A shared data object that is passed between agents in a workflow.
    Each agent can read from and write to this object, enriching it with
    information as the workflow progresses.
    """
    # --- Input Fields ---
    user_query_audio: bytes | None = None
    user_query_text: str | None = None

    # --- Existing Ticket Ingestion Fields ---
    ticket: TicketContext | None = None
    customer: CustomerContext | None = None

    # --- Agent-Populated Fields ---
    language: str | None = None
    classification: dict[str, Any] | None = None
    tool_call: ToolCall | None = None
    tool_output: Any | None = None
    suggested_response: str | None = None
    internal_notes: list[str] = Field(default_factory=list)