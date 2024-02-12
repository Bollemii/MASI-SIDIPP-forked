from abc import ABC, abstractmethod

from src.domain.entities.member import Member
from src.presentation.network.client import Client


class IParentConnection(ABC):
    """Interface for the ParentConnection class."""

    @abstractmethod
    def execute(self, community_id: str) -> Member | None:
        """Connect to a member as parent of the community."""

    @abstractmethod
    def response(self, client: Client, community_id: str, auth_key: str):
        """Response to a parent connection request"""
