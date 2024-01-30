from abc import ABC, abstractmethod

from src.presentation.formatting.message_dataclass import MessageDataclass


class IArchitectureManager(ABC):
    """Interface for the ArchitectureManager class."""

    @abstractmethod
    def share(
        self,
        message: MessageDataclass,
        community_id: str,
        excluded_auth_keys: list[str] | None = None,
    ):
        """Share a message to all members off architecture of a community (except the author and specified excluded_auth_keys)."""
