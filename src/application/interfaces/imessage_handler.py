from abc import ABC, abstractmethod

from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.network.client import Client


class IMessageHandler(ABC):
    """Interface for message handlers."""

    @abstractmethod
    def handle_message(self, client: Client, message: MessageDataclass):
        """Method to handle a message"""
