"""Ticket ingestion workflow placeholder."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.shared_context import (
    CustomerContext,
    SharedContext,
    TicketContext,
)
from app.agents.supervisor_agent import SupervisorAgent
from app.llm_providers.ollama_provider import ollama_provider
from app.models.ticket import Ticket


class TicketIngestionWorkflow:
    """Orchestrates the end-to-end process of analyzing a new ticket."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.supervisor = SupervisorAgent(llm_provider=ollama_provider)

    async def run(self, ticket: Ticket) -> SharedContext:
        """Executes the full ingestion and analysis workflow for a ticket."""
        # 1. Create the initial shared context from the ticket data.
        initial_context = SharedContext(
            ticket=TicketContext.model_validate(ticket),
            customer=CustomerContext.model_validate(ticket.customer),
        )

        # 2. Run the agentic workflow, orchestrated by the Supervisor.
        final_context = await self.supervisor.run(initial_context)

        # 3. Post-process the results (e.g., save to DB, send notifications).
        return final_context
