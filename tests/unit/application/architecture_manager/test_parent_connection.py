from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.architecture_manager.parent_connection import ParentConnection
from src.domain.entities.member import Member
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader


class TestParentConnection:
    """Unit tests for the ParentConnection class."""

    @pytest.fixture(scope="function", autouse=True, name="parent_connection")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    @mock.patch(
        "src.application.interfaces.imessage_formatter", name="message_formatter"
    )
    @mock.patch("src.application.interfaces.imachine_service", name="machine_service")
    def create_parent_connection(
        self,
        member_repository: MagicMock,
        message_formatter: MagicMock,
        machine_service: MagicMock,
    ):
        """Create ParentConnection instance."""
        return ParentConnection(member_repository, message_formatter, machine_service)

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_search_parent(
        self, mock_client: MagicMock, parent_connection: ParentConnection
    ):
        """Test search parent method"""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        parent_connection.machine_service.get_current_user.return_value = Member(
            "abc", "127.0.0.0", 0
        )
        parent_connection.member_repository.get_older_members_from_community.return_value = (
            members
        )
        mock_client.connect_to_server.side_effect = [Exception(), None]
        mock_client.receive_message.return_value = (
            MessageDataclass(MessageHeader.ACCEPT),
            None,
        )

        community_id = "community_id"
        parent = parent_connection.execute(community_id)

        assert parent in members

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_search_parent_not_receive_accept(
        self, mock_client: MagicMock, parent_connection: ParentConnection
    ):
        """Test search parent method if not receive accept message"""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        parent_connection.machine_service.get_current_user.return_value = Member(
            "abc", "127.0.0.0", 0
        )
        parent_connection.member_repository.get_older_members_from_community.return_value = (
            members
        )
        mock_client.connect_to_server.side_effect = [Exception(), None]
        mock_client.receive_message.return_value = (None, None)

        community_id = "community_id"
        parent = parent_connection.execute(community_id)

        assert parent is None

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_search_parent_no_members(
        self, mock_client: MagicMock, parent_connection: ParentConnection
    ):
        """Test search parent method if not receive pong message"""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        parent_connection.machine_service.get_current_user.return_value = Member(
            "abc", "127.0.0.0", 0
        )
        parent_connection.member_repository.get_older_members_from_community.return_value = (
            members
        )
        mock_client.connect_to_server.side_effect = Exception()
        mock_client.receive_message.return_value = (
            MessageDataclass(MessageHeader.ACCEPT),
            None,
        )

        community_id = "community_id"
        parent = parent_connection.execute(community_id)

        assert parent is None

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_search_parent_send_parent_request(
        self, mock_client: MagicMock, parent_connection: ParentConnection
    ):
        """Test search parent method should send parent request"""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        parent_connection.machine_service.get_current_user.return_value = Member(
            "abc", "127.0.0.0", 0
        )
        parent_connection.member_repository.get_older_members_from_community.return_value = (
            members
        )
        mock_client.connect_to_server.side_effect = [Exception(), None]
        mock_client.receive_message.return_value = (
            MessageDataclass(MessageHeader.ACCEPT),
            None,
        )

        parent_connection.execute("community_id")

        message = MessageDataclass(MessageHeader.REQUEST_PARENT, "abc", "community_id")
        mock_client.send_message.assert_any_call(message)

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_search_parent_update_relationship(
        self, mock_client: MagicMock, parent_connection: ParentConnection
    ):
        """Test search parent method should update relationship"""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        parent_connection.machine_service.get_current_user.return_value = Member(
            "abc", "127.0.0.0", 0
        )
        parent_connection.member_repository.get_older_members_from_community.return_value = (
            members
        )
        mock_client.connect_to_server.side_effect = [Exception(), None]
        mock_client.receive_message.return_value = (
            MessageDataclass(MessageHeader.ACCEPT),
            None,
        )

        community_id = "community_id"
        parent_connection.execute(community_id)

        parent_connection.member_repository.update_member_relationship.assert_called_once()

    @mock.patch("src.application.interfaces.iclient_socket", name="client")
    def test_response_update_relationship(
        self, client: MagicMock, parent_connection: ParentConnection
    ):
        """Test response method should update relationship"""
        parent_connection.response(client, "community_id", "content")

        parent_connection.member_repository.update_member_relationship.assert_called_once()

    @mock.patch("src.application.interfaces.iclient_socket", name="client")
    def test_response_send_accept_message(
        self, client: MagicMock, parent_connection: ParentConnection
    ):
        """Test response method should update relationship"""
        parent_connection.response(client, "community_id", "content")

        message = MessageDataclass(MessageHeader.ACCEPT)
        client.send_message.assert_called_once_with(message)
