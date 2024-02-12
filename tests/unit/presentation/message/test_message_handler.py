from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.presentation.handler.message_handler import MessageHandler
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.application.exceptions.message_error import MessageError


class TestMessageHandler:
    """Test class for MessageHandler"""

    @pytest.fixture(scope="function", autouse=True, name="message_handler")
    @mock.patch(
        "src.application.interfaces.icommunity_service", name="mock_community_service"
    )
    @mock.patch(
        "src.application.interfaces.iarchitecture_manager",
        name="mock_architecture_manager",
    )
    @mock.patch("src.application.interfaces.isave_member", name="mock_save_member")
    @mock.patch("src.application.interfaces.isave_idea", name="mock_save_idea")
    @mock.patch("src.application.interfaces.isave_opinion", name="mock_save_opinion")
    @mock.patch(
        "src.application.interfaces.ijoin_community", name="join_community_usecase"
    )
    def create_message_handler(
        self,
        join_community_usecase: MagicMock,
        mock_save_opinion: MagicMock,
        mock_save_idea: MagicMock,
        mock_save_member: MagicMock,
        mock_architecture_manager: MagicMock,
        mock_community_service: MagicMock,
    ) -> MessageHandler:
        """Fixture to create a MessageHandler instance."""
        mock_community_service.is_community_member.return_value = True
        return MessageHandler(
            mock_community_service,
            mock_architecture_manager,
            join_community_usecase,
            mock_save_member,
            mock_save_idea,
            mock_save_opinion,
        )

    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_handle_message(
        self,
        mock_client: MagicMock,
        message_handler: MessageHandler,
    ):
        """Test method for handle_message with different MessageHeader."""
        message = MessageDataclass(MessageHeader.INVITATION, "content")
        sender = ("127.0.0.1", 1024)
        message_handler.handle_message(sender, mock_client, message)

        message_handler.join_community_usecase.execute.assert_called_once()

    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_invalid_handler_message(
        self, mock_client: MagicMock, message_handler: MessageHandler
    ):
        """Test method for handle_message with invalid MessageDataclass."""
        invalid_message = MessageDataclass(header="INVALID_HEADER", content="content")
        sender = ("127.0.0.1", 1024)

        with pytest.raises(MessageError):
            message_handler.handle_message(sender, mock_client, invalid_message)

    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_invalid_community_member(
        self, mock_client: MagicMock, message_handler: MessageHandler
    ):
        """Test method for handle_message with invalid community member."""
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content")
        sender = ("127.0.0.1", 1024)

        message_handler.community_service.is_community_member.return_value = False

        with pytest.raises(MessageError):
            message_handler.handle_message(sender, mock_client, message)

    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_valid_community_member(
        self, mock_client: MagicMock, message_handler: MessageHandler
    ):
        """Test method for handle_message with valid community member."""
        message = MessageDataclass(MessageHeader.CREATE_IDEA, "content")
        sender = ("127.0.0.1", 1024)
        message_handler.handle_message(sender, mock_client, message)

        message_handler.save_idea_usecase.execute.assert_called_once()

    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_save_opinion_call(
        self, mock_client: MagicMock, message_handler: MessageHandler
    ):
        """Test method for handle_message with valid community member."""
        message = MessageDataclass(MessageHeader.CREATE_OPINION, "content")
        sender = ("127.0.0.1", 1024)
        message_handler.handle_message(sender, mock_client, message)

        message_handler.save_opinion_usecase.execute.assert_called_once()

    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_save_member_call(
        self, mock_client: MagicMock, message_handler: MessageHandler
    ):
        """Test method for handle_message with valid community member."""
        message = MessageDataclass(MessageHeader.ADD_MEMBER, "content")
        sender = ("127.0.0.1", 1024)
        message_handler.handle_message(sender, mock_client, message)

        message_handler.save_member_usecase.execute.assert_called_once()

    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_receive_ping(
        self, mock_client: MagicMock, message_handler: MessageHandler
    ):
        """Test method for handle ping message"""
        message = MessageDataclass(MessageHeader.PING)
        sender = ("127.0.0.1", 1024)
        message_handler.handle_message(sender, mock_client, message)

        mock_client.send_message.assert_called_once_with(
            MessageDataclass(MessageHeader.PONG)
        )
