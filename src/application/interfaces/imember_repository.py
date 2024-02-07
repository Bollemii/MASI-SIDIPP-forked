from abc import ABC, abstractmethod
from typing import Literal

from src.domain.entities.member import Member


class IMemberRepository(ABC):
    """Interface for the member repository class"""

    @abstractmethod
    def initialize_if_not_exists(self, target_database: str):
        """Initialize the requirements"""

    @abstractmethod
    def add_member_to_community(
        self,
        community_id: str,
        member: Member,
        relationship: Literal["parent", "child"] | None = None,
    ) -> None:
        """Add a member to a specific community"""

    @abstractmethod
    def clear_members_relationship(
        self,
        community_id: str,
    ) -> None:
        """Clear the relationship of all members"""

    @abstractmethod
    def update_member_relationship(
        self,
        community_id: str,
        auth_key: str,
        relationship: Literal["parent", "child"] | None,
    ):
        """Update the relationship of a member in a specific community"""

    @abstractmethod
    def get_member_for_community(
        self,
        community_id: str,
        member_auth_key: str | None = None,
        ip_address: str | None = None,
    ) -> Member | None:
        """Get a member of a specific community"""

    @abstractmethod
    def get_members_from_community(
        self, community_id: str, is_related: bool = False
    ) -> list[Member]:
        """Get all members of a specific community"""
