from abc import ABC, abstractmethod


class IDeconnection(ABC):
    """Interface for the Deconnection class."""

    @abstractmethod
    def execute(self):
        """Deconnect of all communities"""
