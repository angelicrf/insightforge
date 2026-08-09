"""Agent for selecting the correct tool based on user query."""

from typing import Any

import structlog

from .base_agent import BaseAgent
from .shared_context import SharedContext, ToolCall

log = structlog.get_logger()


class ToolSelectionAgent(BaseAgent):
    """
    An agent that analyzes the user's query and selects the appropriate
    tool and function to call.
    """

    def __init__(self, llm_provider: Any):
        super().__init__(llm_provider)

    @property
    def name(self) -> str:
        return "ToolSelectionAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        """
        Determines which tool to use based on the user's text query.

        In a real implementation, this would use an LLM with function-calling
        capabilities to parse the user's intent and select a tool. Here, we
        use simple keyword matching as a placeholder.
        """
        if not context.user_query_text or context.tool_call:
            return context

        log.info("Selecting tool for user query...", query=context.user_query_text)
        query = context.user_query_text.lower()

        if "case" in query and "salesforce" in query:
            # Placeholder for extracting case ID
            case_id = "001xx000003DGZzAAO"  # Example ID
            context.tool_call = ToolCall(tool_name="salesforce", function_name="get_case_details", args={"case_id": case_id})
            log.info("Selected Salesforce tool.", tool_call=context.tool_call)
        elif "table" in query and ("list" in query or "show" in query):
            context.tool_call = ToolCall(tool_name="neondb", function_name="list_tables", args={})
            log.info("Selected NeonDB tool.", tool_call=context.tool_call)
        else:
            log.info("No specific tool identified. Proceeding to response generation.")
            context.tool_call = ToolCall(tool_name="none", function_name="none", args={})

        return context