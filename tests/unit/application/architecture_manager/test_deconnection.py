from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.architecture_manager.deconnection import Deconnection
from src.domain.entities.community import Community


class TestDeconnection:
    """Test the deconnection method of the ArchitectureManager class."""

    @pytest.fixture(scope="function", autouse=True, name="deconnection")
    @mock.patch(
        "src.application.interfaces.ishare_information", name="share_information"
    )
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    @mock.patch(
        "src.application.interfaces.icommunity_repository", name="community_repository"
    )
    def create_deconnection(
        self,
        community_repository: MagicMock,
        member_repository: MagicMock,
        share_information: MagicMock,
    ) -> Deconnection:
        """Create a deconnection instance"""
        community_repository.get_communities.return_value = [
            Community("abc", "name", "description")
        ]
        return Deconnection(
            community_repository,
            member_repository,
            share_information,
        )

    def test_deconnection_get_communities_list(self, deconnection: Deconnection):
        """Test that the method get communities list"""
        deconnection.execute()

        deconnection.community_repository.get_communities.assert_called_once()

    def test_deconnection_share_deconnect_message(self, deconnection: Deconnection):
        """Test that the method share the deconnection message"""
        deconnection.execute()

        deconnection.share_information.execute.assert_called()

    def test_deconnection_clear_relationship(self, deconnection: Deconnection):
        """Test that the method clear the relationship"""
        deconnection.execute()

        deconnection.member_repository.clear_members_relationship.assert_called()
