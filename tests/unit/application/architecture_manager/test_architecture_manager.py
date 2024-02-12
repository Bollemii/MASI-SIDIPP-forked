from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.application.architecture_manager.architecture_manager import (
    ArchitectureManager,
)


class TestArchitectureManager:
    """Test cases for the ArchitectureManager class."""

    @pytest.fixture(scope="function", autouse=True, name="architecture_manager")
    @mock.patch("src.application.interfaces.ideconnection", name="deconnection")
    @mock.patch(
        "src.application.interfaces.iparent_connection", name="parent_connection"
    )
    @mock.patch(
        "src.application.interfaces.ishare_information", name="share_information"
    )
    def create_architecture_manager(
        self,
        share_information: MagicMock,
        parent_connection: MagicMock,
        deconnection: MagicMock,
    ):
        """Create ArchitectureManager instance."""
        return ArchitectureManager(share_information, parent_connection, deconnection)

    def test_share_information(self, architecture_manager: ArchitectureManager):
        """Test share method call share method from ShareInformation"""
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", "community_id")
        community_id = "community_id"
        excluded_auth_keys = ["auth_key"]
        excluded_ip_addresses = ["ip_address"]

        architecture_manager.share_information(
            message, community_id, excluded_auth_keys, excluded_ip_addresses
        )

        architecture_manager.share_information_usecase.execute.assert_called_once()

    def test_connect_to_parent(self, architecture_manager: ArchitectureManager):
        """Test connect_to_parent method call execute method from ParentConnection"""
        community_id = "community_id"

        architecture_manager.connect_to_parent(community_id)

        architecture_manager.parent_connection_usecase.execute.assert_called_once()

    def test_response_parent_request(self, architecture_manager: ArchitectureManager):
        """Test response_parent_request call response method of ParentConnection"""
        client = MagicMock()
        community_id = "community_id"
        auth_key = "auth_key"

        architecture_manager.response_parent_request(client, community_id, auth_key)

        architecture_manager.parent_connection_usecase.response.assert_called_once()

    def test_deconnection(self, architecture_manager: ArchitectureManager):
        """Test deconnection call execute method of Deconnection"""
        architecture_manager.deconnection()

        architecture_manager.deconnection_usecase.execute.assert_called_once()

    def test_deconnect_member(self, architecture_manager: ArchitectureManager):
        """Test deconnect_member call deconnect_member method of Deconnection"""
        community_id = "community_id"
        auth_key = "auth_key"

        architecture_manager.deconnect_member(community_id, auth_key)

        architecture_manager.deconnection_usecase.deconnect_member.assert_called_once()
