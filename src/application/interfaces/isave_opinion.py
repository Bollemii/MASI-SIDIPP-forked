from abc import ABC, abstractmethod


class ISaveOpinion(ABC):
    """Interface for the SaveOpinion use case."""

    @abstractmethod
    def execute(self, community_id: str, message: str) -> str:
        """Save an opinion."""
