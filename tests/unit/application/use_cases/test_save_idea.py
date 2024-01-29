from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.save_idea import SaveIdea


class TestSaveIdea:
    """Unit tests for the SaveIdea use case."""

    @pytest.fixture(scope="function", autouse=True, name="idea_repository")
    @mock.patch(
        "src.application.interfaces.iidea_repository", name="mock_idea_repository"
    )
    def create_idea_repository(self, mock_idea_repository: MagicMock) -> MagicMock:
        """Create a SaveIdea instance."""
        return mock_idea_repository

    @pytest.fixture(scope="function", autouse=True, name="symetric_encryption_service")
    @mock.patch(
        "src.application.interfaces.isymetric_encryption_service",
        name="mock_symetric_encryption_service",
    )
    def create_symetric_encryption_service(
        self, mock_symetric_encryption_service: MagicMock
    ) -> MagicMock:
        """Create a symetric encryption service instance"""
        mock_symetric_encryption_service.decrypt.return_value = (
            "identifier,content,author_id,1970-01-01T00:00:00"
        )
        return mock_symetric_encryption_service

    @pytest.fixture(scope="function", autouse=True, name="community_manager")
    @mock.patch(
        "src.application.interfaces.icommunity_manager",
        name="mock_community_manager",
    )
    def create_community_manager(self, mock_community_manager: MagicMock) -> MagicMock:
        """Create a community manager instance"""
        mock_community_manager.get_community_symetric_key.return_value = "symetric_key"
        return mock_community_manager

    @pytest.fixture(scope="function", autouse=True, name="save_idea")
    def create_save_idea(
        self,
        symetric_encryption_service: MagicMock,
        community_manager: MagicMock,
        idea_repository: MagicMock,
    ) -> SaveIdea:
        """Create a SaveIdea instance."""
        return SaveIdea(
            idea_repository,
            symetric_encryption_service,
            community_manager,
        )

    def test_save_idea_successful(self, save_idea: SaveIdea):
        """Test saving an idea."""
        result = save_idea.execute("community_id", "nonce,tag,cipher_idea")

        assert result == "Success!"

    def test_save_idea_failed(self, save_idea: SaveIdea):
        """Test saving an idea."""
        result = save_idea.execute("community_id", "")

        assert result != "Success!"

    def test_save_idea(self, idea_repository: MagicMock, save_idea: SaveIdea):
        """Test saving an idea."""
        save_idea.execute("community_id", "nonce,tag,cipher_idea")

        idea_repository.add_idea_to_community.assert_called_once()

    def test_get_symetric_key(
        self,
        community_manager: MagicMock,
        save_idea: SaveIdea,
    ):
        """Test getting the symetric key."""
        save_idea.execute("community_id", "nonce,tag,cipher_idea")

        community_manager.get_community_symetric_key.assert_called_once()

    def test_decrypt(
        self,
        symetric_encryption_service: MagicMock,
        save_idea: SaveIdea,
    ):
        """Test decrypting the idea."""
        save_idea.execute("community_id", "nonce,tag,cipher_idea")

        symetric_encryption_service.decrypt.assert_called_once()

    def test_is_community_member(
        self,
        community_manager: MagicMock,
        save_idea: SaveIdea,
    ):
        """Test checking if the author is a community member."""
        save_idea.execute("community_id", "nonce,tag,cipher_idea")

        community_manager.is_community_member.assert_called_once()

    def test_save_idea_failed_author_not_member(
        self,
        community_manager: MagicMock,
        save_idea: SaveIdea,
    ):
        """Test saving an idea with an author that is not a member."""
        community_manager.is_community_member.return_value = False

        result = save_idea.execute("community_id", "nonce,tag,cipher_idea")

        assert result != "Success!"
