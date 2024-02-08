from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.save_opinion import SaveOpinion


class TestSaveOpinion:
    """Unit tests for the SaveOpinion use case."""

    @pytest.fixture(scope="function", autouse=True, name="opinion_repository")
    @mock.patch(
        "src.application.interfaces.iopinion_repository", name="mock_opinion_repository"
    )
    def create_opinion_repository(
        self, mock_opinion_repository: MagicMock
    ) -> MagicMock:
        """Create a SaveOpinion instance."""
        return mock_opinion_repository

    @pytest.fixture(scope="function", autouse=True, name="community_manager")
    @mock.patch(
        "src.application.interfaces.icommunity_manager",
        name="mock_community_manager",
    )
    def create_community_manager(self, mock_community_manager: MagicMock) -> MagicMock:
        """Create a community manager instance"""
        mock_community_manager.get_community_symetric_key.return_value = "symetric_key"
        return mock_community_manager

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
            "identifier,content,author_id,1970-01-01T00:00:00,parent_id"
        )
        return mock_symetric_encryption_service

    @pytest.fixture(scope="function", autouse=True, name="save_opinion")
    def create_save_opinion(
        self,
        symetric_encryption_service: MagicMock,
        community_manager: MagicMock,
        opinion_repository: MagicMock,
    ) -> SaveOpinion:
        """Create a SaveOpinion instance."""
        return SaveOpinion(
            opinion_repository,
            symetric_encryption_service,
            community_manager,
        )

    def test_save_opinion_successful(self, save_opinion: SaveOpinion):
        """Test saving an opinion."""
        result = save_opinion.execute("community_id", "nonce,tag,cipher_opinion")

        assert result == "Success!"

    def test_save_opinion_failed(self, save_opinion: SaveOpinion):
        """Test saving an opinion."""
        result = save_opinion.execute("", "")

        assert result != "Success!"

    def test_save_opinion(
        self, opinion_repository: MagicMock, save_opinion: SaveOpinion
    ):
        """Test saving an opinion."""
        save_opinion.execute("community_id", "nonce,tag,cipher_opinion")

        opinion_repository.add_opinion_to_community.assert_called_once()

    def test_get_symetric_key(
        self,
        community_manager: MagicMock,
        save_opinion: SaveOpinion,
    ):
        """Test getting the symetric key."""
        save_opinion.execute("community_id", "nonce,tag,cipher_opinion")

        community_manager.get_community_symetric_key.assert_called_once()

    def test_decrypt(
        self,
        symetric_encryption_service: MagicMock,
        save_opinion: SaveOpinion,
    ):
        """Test decrypting the opinion."""
        save_opinion.execute("community_id", "nonce,tag,cipher_opinion")

        symetric_encryption_service.decrypt.assert_called_once()

    def test_is_community_member(
        self,
        community_manager: MagicMock,
        save_opinion: SaveOpinion,
    ):
        """Test checking if the author is a member of the community."""
        save_opinion.execute("community_id", "nonce,tag,cipher_opinion")

        community_manager.is_community_member.assert_called_once()

    def test_save_opinion_failed_author_not_member(
        self,
        community_manager: MagicMock,
        save_opinion: SaveOpinion,
    ):
        """Saving an opinion with an author that is not a member should return an error message."""
        community_manager.is_community_member.return_value = False
        result = save_opinion.execute("community_id", "nonce,tag,cipher_opinion")

        assert result != "Success!"

    def test_save_opinion_with_invalid_content(
        self,
        save_opinion: SaveOpinion,
    ):
        """Saving an opinion with invalid content should return an error message."""
        save_opinion.symetric_encryption_service.decrypt.return_value = (
            "identifier,c,author_id,1970-01-01T00:00:00,parent_id"
        )

        result = save_opinion.execute("community_id", "nonce,tag,cipher_opinion")

        assert result != "Success!"
        assert result == "Content is too short."
        save_opinion.opinion_repository.add_opinion_to_community.assert_not_called()
