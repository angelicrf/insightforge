"""Abstract base class for all agents."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from .shared_context import SharedContext


class BaseAgent(ABC):
    """
    An abstract base class that defines the standard interface for all agents.

    Each agent is a specialist designed to perform a specific task in the support
    automation workflow. They operate on a shared context object but are
    isolated from one another.
    """

    @abstractmethod
    def __init__(self, llm_provider: Any):
        """
        Initializes the agent with a language model provider.

        Args:
            llm_provider: A language model client.
        """
        self.llm_provider = llm_provider

    @property
    @abstractmethod
    def name(self) -> str:
        """A unique, descriptive name for the agent."""
        ...

    @abstractmethod
    async def run(self, context: SharedContext) -> SharedContext:
        """
        The main execution method for the agent.

        It takes the shared context, performs its specific task, updates the
        context with its results, and returns the modified context.
        """
        ...