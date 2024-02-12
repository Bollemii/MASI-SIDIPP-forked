from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.architecture_manager.deconnection import Deconnection
from src.domain.entities.community import Community


class TestDeconnection:
    """Test the deconnection method of the ArchitectureManager class."""

    @pytest.fixture(scope="function", autouse=True, name="deconnection")
    @mock.patch(
        "src.application.interfaces.iparent_connection", name="parent_connection"
    )
    @mock.patch(
        "src.application.interfaces.ishare_information", name="share_information"
    )
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    @mock.patch("src.application.interfaces.imachine_service", name="machine_service")
    @mock.patch(
        "src.application.interfaces.icommunity_repository", name="community_repository"
    )
    def create_deconnection(
        self,
        community_repository: MagicMock,
        machine_service: MagicMock,
        member_repository: MagicMock,
        share_information: MagicMock,
        parent_connection: MagicMock,
    ) -> Deconnection:
        """Create a deconnection instance"""
        community_repository.get_communities.return_value = [
            Community("abc", "name", "description")
        ]
        return Deconnection(
            community_repository,
            machine_service,
            member_repository,
            share_information,
            parent_connection,
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

    def test_deconnection_deconnect_member(self, deconnection: Deconnection):
        """Test that the method deconnect member should update the member relationship"""
        deconnection.deconnect_member("abc", "auth_key")

        deconnection.member_repository.update_member_relationship.assert_called()

    def test_deconnection_deconnect_member_parent(self, deconnection: Deconnection):
        """Test that the method deconnect member
        should connect to parent if the member is a parent"""
        deconnection.member_repository.get_member_for_community.return_value.relationship = (
            "parent"
        )

        deconnection.deconnect_member("abc", "auth_key")

        deconnection.parent_connection.execute.assert_called()

    def test_deconnection_deconnect_member_child(self, deconnection: Deconnection):
        """Test that the method deconnect member does
        not connect to parent if the member is a child"""
        deconnection.member_repository.get_member_for_community.return_value.relationship = (
            "child"
        )

        deconnection.deconnect_member("abc", "auth_key")

        deconnection.parent_connection.execute.assert_not_called()
