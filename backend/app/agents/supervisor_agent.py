"""The Supervisor Agent: The central orchestrator of the agentic workflow."""

from typing import Any

import structlog

from .base_agent import BaseAgent
from .shared_context import SharedContext
from .tool_selection_agent import ToolSelectionAgent
from .voice_to_text_agent import VoiceToTextAgent
from ..tools.neondb_client import NeonDBTool
from ..tools.salesforce_client import SalesforceTool


log = structlog.get_logger()

class SupervisorAgent(BaseAgent):
    """
    The Supervisor Agent orchestrates the entire ticket resolution process.

    It does not perform tasks itself but instead analyzes the shared context
    and decides which specialized agent to delegate the task to next. It is
    the entry point and the controller of the agentic workflow, ensuring tasks
    are performed in the correct order.
    """

    def __init__(self, llm_provider: Any):
        super().__init__(llm_provider)
        # In a real app, these would be configured and injected
        self.voice_agent = VoiceToTextAgent(llm_provider)
        self.tool_selection_agent = ToolSelectionAgent(llm_provider)
        self.salesforce_tool = SalesforceTool()
        # TODO: Securely provide admin token and base URL
        self.neondb_tool = NeonDBTool(internal_api_base_url="http://127.0.0.1:8000", admin_token="dev-admin-token")

    @property
    def name(self) -> str:
        return "SupervisorAgent"

    async def _execute_tool(self, context: SharedContext) -> SharedContext:
        """Executes the tool call decided by the ToolSelectionAgent."""
        if not context.tool_call or context.tool_call.tool_name == "none":
            return context

        log.info("Executing tool call", tool_call=context.tool_call)
        tool_name = context.tool_call.tool_name
        function_name = context.tool_call.function_name
        args = context.tool_call.args

        try:
            if tool_name == "salesforce":
                method = getattr(self.salesforce_tool, function_name)
                context.tool_output = await method(**args)
            elif tool_name == "neondb":
                method = getattr(self.neondb_tool, function_name)
                context.tool_output = await method(**args)
            else:
                log.warning("Unknown tool specified", tool_name=tool_name)
                context.tool_output = {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            log.error("Error executing tool", error=str(e))
            context.tool_output = {"error": str(e)}

        log.info("Tool execution finished.", output=context.tool_output)
        return context

    async def run(self, context: SharedContext) -> SharedContext:
        """Orchestrates the agentic workflow based on the shared context."""
        log.info("Supervisor starting workflow.", initial_context=context.model_dump(exclude_none=True))

        # 1. Voice-to-Text (if audio is present)
        context = await self.voice_agent.run(context)

        # 2. Tool Selection (if text is present)
        context = await self.tool_selection_agent.run(context)

        # 3. Tool Execution (if a tool was selected)
        context = await self._execute_tool(context)

        # 4. Response Generation (future step)
        # An agent would take the tool_output and generate a natural language response.
        if context.tool_output:
            context.suggested_response = f"I found this information: {context.tool_output}"

        log.info("Supervisor finished workflow.", final_context=context.model_dump(exclude_none=True))
        return context