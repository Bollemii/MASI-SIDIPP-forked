from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.save_member import SaveMember


class TestSaveMember:
    """Unit tests for the save member use case."""

    @pytest.fixture(scope="function", autouse=True, name="save_member")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="mock_member_repository"
    )
    @mock.patch(
        "src.application.interfaces.icommunity_service", name="mock_community_service"
    )
    @mock.patch(
        "src.application.interfaces.isymetric_encryption_service",
        name="mock_symetric_encryption_service",
    )
    def create_save_member_usecase(
        self,
        mock_symetric_encryption_service: MagicMock,
        mock_community_service: MagicMock,
        mock_member_repository: MagicMock,
    ) -> SaveMember:
        """Fixture to create a SaveMember instance."""
        mock_symetric_encryption_service.decrypt.return_value = (
            "auth_code,127.0.0.1,1664,1970-01-01T00:00:00,None"
        )
        return SaveMember(
            mock_member_repository,
            mock_community_service,
            mock_symetric_encryption_service,
        )

    def test_save_member_successful(
        self,
        save_member: SaveMember,
    ):
        """Test saving a member."""
        result = save_member.execute("community_id", "nonce,tag,cipher_member")

        assert result == "Success!"

    def test_save_member_unsuccessful(
        self,
        save_member: SaveMember,
    ):
        """Test saving a member."""
        save_member.symetric_encryption_service.decrypt.side_effect = Exception("Error")

        result = save_member.execute("community_id", "nonce,tag,cipher_member")

        assert result != "Success!"

    def test_save_member_call_get_symetric_key(
        self,
        save_member: SaveMember,
    ):
        """Test saving a member."""
        save_member.execute("community_id", "nonce,tag,cipher_member")

        save_member.community_service.get_community_symetric_key.assert_called_once()

    def test_save_member_call_decrypt(
        self,
        save_member: SaveMember,
    ):
        """Test saving a member."""
        save_member.execute("community_id", "nonce,tag,cipher_member")

        save_member.symetric_encryption_service.decrypt.assert_called_once()

    def test_save_member_call_add_member_to_community(
        self,
        save_member: SaveMember,
    ):
        """Test saving a member."""
        save_member.execute("community_id", "nonce,tag,cipher_member")

        save_member.member_repository.add_member_to_community.assert_called_once()
