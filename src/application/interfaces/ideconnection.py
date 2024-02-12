from abc import ABC, abstractmethod


class IDeconnection(ABC):
    """Interface for the Deconnection class."""

    @abstractmethod
    def execute(self):
        """Deconnect of all communities"""

    @abstractmethod
    def deconnect_member(self, community_id: str, auth_key: str):
        """Deconnect a member from a community"""
