from abc import ABC, abstractmethod

from src.domain.entities.member import Member
from src.presentation.formatting.message_dataclass import MessageDataclass


class IArchitectureManager(ABC):
    """Interface for the ArchitectureManager class."""

    @abstractmethod
    def share_information(
        self,
        message: MessageDataclass,
        community_id: str,
        excluded_auth_keys: list[str] = [],
        excluded_ip_addresses: list[str] = [],
    ):
        """Share a message to related members of architecture in a community
        (except the author and specified excluded)."""

    @abstractmethod
    def connect_to_parent(self, community_id: str) -> Member | None:
        """Connect to a member as parent of the community."""

    @abstractmethod
    def deconnection(self):
        """Deconnect of all communities"""
