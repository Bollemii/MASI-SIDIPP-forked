from abc import ABC, abstractmethod


class ICommunityManager(ABC):
    """Interface for Community Manager"""

    @abstractmethod
    def get_community_symetric_key(self, community_id: str) -> str:
        """Get community symetric key"""

    @abstractmethod
    def is_community_member(
        self,
        community_id: str,
        auth_key: str | None = None,
        ip_address: str | None = None,
    ) -> bool:
        """Check if user is member of community"""
