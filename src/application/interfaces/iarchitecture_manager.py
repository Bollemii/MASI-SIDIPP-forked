from abc import ABC, abstractmethod

from src.presentation.formatting.message_dataclass import MessageDataclass


class IArchitectureManager(ABC):
    """Interface for the ArchitectureManager class."""

    @abstractmethod
    def share(
        self,
        message: MessageDataclass,
        community_id: str,
        excluded_auth_keys: list[str] = [],
        excluded_ip_addresses: list[str] = [],
    ):
        """Share a message to related members of architecture in a community
        (except the author and specified excluded)."""
