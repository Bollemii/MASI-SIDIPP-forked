from abc import ABC, abstractmethod


class ISaveMember(ABC):
    """Interface for the SaveMember use case."""

    @abstractmethod
    def execute(self, community_id: str, message: str) -> str:
        """Save a member."""
