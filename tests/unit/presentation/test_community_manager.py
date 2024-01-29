from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.presentation.manager.community_manager import CommunityManager


class TestCommunityManager:
    """Test CommunityManager class"""

    @pytest.fixture(scope="function", autouse=True, name="community_repository")
    @mock.patch(
        "src.application.interfaces.icommunity_repository",
        name="mock_community_repository",
    )
    def create_community_repository(
        self, mock_community_repository: MagicMock
    ) -> MagicMock:
        """Create a CommunityRepository instance."""
        mock_community_repository.get_community_encryption_key_path.return_value = (
            "symetric_key_path"
        )
        return mock_community_repository

    @pytest.fixture(scope="function", autouse=True, name="member_repository")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="mock_member_repository"
    )
    def create_member_repository(self, mock_member_repository: MagicMock) -> MagicMock:
        """Create a MemberRepository instance."""
        return mock_member_repository

    @pytest.fixture(scope="function", autouse=True, name="file_service")
    @mock.patch("src.application.interfaces.ifile_service", name="mock_file_service")
    def create_file_service(self, mock_file_service: MagicMock) -> MagicMock:
        """Create a FileService instance."""
        return mock_file_service

    @pytest.fixture(scope="function", autouse=True, name="community_manager")
    def create_community_manager(
        self,
        community_repository: MagicMock,
        member_repository: MagicMock,
        file_service: MagicMock,
    ) -> CommunityManager:
        """Create a CommunityManager instance."""
        return CommunityManager(community_repository, member_repository, file_service)

    def test_get_community_symetric_key(
        self,
        community_manager: CommunityManager,
        file_service: MagicMock,
    ):
        """Test method for get_community_symetric_key."""
        file_service.read_file.return_value = "symetric_key"

        symetric_key = community_manager.get_community_symetric_key("community_id")

        assert symetric_key == "symetric_key"

    def test_is_community_member_auth_key(
        self,
        community_manager: CommunityManager,
        member_repository: MagicMock,
    ):
        """Test method for is_community_member."""
        member_repository.get_member_for_community.return_value = "member"

        is_member = community_manager.is_community_member(
            "community_id", auth_key="auth_key"
        )

        assert is_member is True

    def test_is_not_community_member_auth_key(
        self,
        community_manager: CommunityManager,
        member_repository: MagicMock,
    ):
        """Test method for is_community_member."""
        member_repository.get_member_for_community.return_value = None

        is_member = community_manager.is_community_member(
            "community_id", auth_key="auth_key"
        )

        assert is_member is False

    def test_is_community_member_ip_address(
        self,
        community_manager: CommunityManager,
        member_repository: MagicMock,
    ):
        """Test method for is_community_member."""
        member_repository.get_member_for_community.return_value = "member"

        is_member = community_manager.is_community_member(
            "community_id", ip_address="ip_address"
        )

        assert is_member is True

    def test_is_not_community_member_ip_address(
        self,
        community_manager: CommunityManager,
        member_repository: MagicMock,
    ):
        """Test method for is_community_member."""
        member_repository.get_member_for_community.return_value = None

        is_member = community_manager.is_community_member(
            "community_id", ip_address="ip_address"
        )

        assert is_member is False
