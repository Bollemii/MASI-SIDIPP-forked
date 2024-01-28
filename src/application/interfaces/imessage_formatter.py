from abc import ABC, abstractmethod

from src.presentation.formatting.message_dataclass import MessageDataclass


class IMessageFormatter(ABC):
    """Interface to format and parse message objects"""

    @abstractmethod
    def format(self, message: MessageDataclass) -> str:
        """Method to format a message object to message string"""

    @abstractmethod
    def parse(self, formated_message: str) -> MessageDataclass:
        """Method to parse the message string to a message object"""
