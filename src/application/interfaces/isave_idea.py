from abc import ABC, abstractmethod


class ISaveIdea(ABC):
    """Interface for the SaveIdea use case."""

    @abstractmethod
    def execute(self, community_id: str, message: str) -> str:
        """Save an idea."""
