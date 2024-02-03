from unittest import mock
from unittest.mock import MagicMock
import pytest
from src.domain.entities.member import Member
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader

from src.presentation.manager.architecture_manager import ArchitectureManager


class TestArchitectureManager:
    """Test cases for the ArchitectureManager class."""

    @pytest.fixture(scope="function", autouse=True, name="architecture_manager")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    @mock.patch(
        "src.application.interfaces.imessage_formatter", name="message_formatter"
    )
    @mock.patch("src.application.interfaces.imachine_service", name="machine_service")
    def create_architecture_manager(
        self,
        member_repository: MagicMock,
        message_formatter: MagicMock,
        machine_service: MagicMock,
    ):
        """Create ArchitectureManager instance."""
        return ArchitectureManager(
            member_repository, message_formatter, machine_service
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_share_get_members(
        self, mock_client: MagicMock, architecture_manager: ArchitectureManager
    ):
        """Test share method."""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "community_id"
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", community_id)

        architecture_manager.member_repository.get_members_from_community.return_value = (
            members
        )
        architecture_manager.machine_service.get_current_user.return_value = members[0]

        architecture_manager.share(message, community_id)

        architecture_manager.member_repository.get_members_from_community.assert_called_once()
        architecture_manager.machine_service.get_current_user.assert_called_once()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_share_send_message(
        self, mock_client: MagicMock, architecture_manager: ArchitectureManager
    ):
        """Test share method."""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "community_id"
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", community_id)

        architecture_manager.member_repository.get_members_from_community.return_value = (
            members
        )
        architecture_manager.machine_service.get_current_user.return_value = members[0]

        architecture_manager.share(message, community_id)

        mock_client.connect_to_server.assert_called()
        mock_client.send_message.assert_called()
        mock_client.close_connection.assert_called()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_share_send_message_count(
        self, mock_client: MagicMock, architecture_manager: ArchitectureManager
    ):
        """Test share method."""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "community_id"
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", community_id)

        architecture_manager.member_repository.get_members_from_community.return_value = (
            members
        )
        architecture_manager.machine_service.get_current_user.return_value = members[0]

        architecture_manager.share(message, community_id)

        assert mock_client.send_message.call_count == 2

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_share_send_message_count_with_excluded(
        self, mock_client: MagicMock, architecture_manager: ArchitectureManager
    ):
        """Test share method."""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "community_id"
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", community_id)
        excluded_auth_keys = ["abc2"]

        architecture_manager.member_repository.get_members_from_community.return_value = (
            members
        )
        architecture_manager.machine_service.get_current_user.return_value = members[0]

        architecture_manager.share(message, community_id, excluded_auth_keys)

        assert mock_client.send_message.call_count == 1

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_share_send_message_count_with_all_excluded(
        self, mock_client: MagicMock, architecture_manager: ArchitectureManager
    ):
        """Test share method."""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "community_id"
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", community_id)
        excluded_auth_keys = ["abc", "abc2", "abc3"]

        architecture_manager.member_repository.get_members_from_community.return_value = (
            members
        )
        architecture_manager.machine_service.get_current_user.return_value = members[0]

        architecture_manager.share(message, community_id, excluded_auth_keys)

        mock_client.send_message.assert_not_called()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_share_send_message_count_with_no_members(
        self, mock_client: MagicMock, architecture_manager: ArchitectureManager
    ):
        """Test share method."""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "community_id"
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", community_id)

        architecture_manager.member_repository.get_members_from_community.return_value = (
            []
        )
        architecture_manager.machine_service.get_current_user.return_value = members[0]

        architecture_manager.share(message, community_id)

        mock_client.send_message.assert_not_called()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_share_socket_error(
        self, mock_client: MagicMock, architecture_manager: ArchitectureManager
    ):
        """Test share method."""
        mock_client.return_value = mock_client
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "community_id"
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content", community_id)

        architecture_manager.member_repository.get_members_from_community.return_value = (
            members
        )
        architecture_manager.machine_service.get_current_user.return_value = members[0]
        mock_client.connect_to_server.side_effect = Exception()

        architecture_manager.share(message, community_id)

        mock_client.send_message.assert_not_called()
