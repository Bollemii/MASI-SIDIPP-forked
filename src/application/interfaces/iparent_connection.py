from abc import ABC, abstractmethod

from src.domain.entities.member import Member


class IParentConnection(ABC):
    """Interface for the ParentConnection class."""

    @abstractmethod
    def execute(self, community_id: str) -> Member | None:
        """Connect to a member as parent of the community."""
