from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.presentation.handler.message_handler import MessageHandler
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.application.exceptions.message_error import MessageError


class TestMessageHandler:
    """Test class for MessageHandler"""

    @pytest.fixture(scope="function", autouse=True, name="message")
    def create_message(self):
        """Fixture to create a MessageDataclass with different MessageHeader."""
        header = MessageHeader.INVITATION
        content = "content"
        return MessageDataclass(header=header, content=content)

    @mock.patch(
        "src.application.interfaces.ijoin_community", name="mock_join_community"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_handle_message(
        self,
        mock_client: MagicMock,
        mock_join_community: MagicMock,
        message: MessageDataclass,
    ):
        """Test method for handle_message with different MessageHeader."""
        message_handler = MessageHandler(mock_join_community)

        message_handler.handle_message(mock_client, message)

        mock_join_community.execute.assert_called_once()

    @mock.patch(
        "src.application.interfaces.ijoin_community", name="mock_join_community"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def test_invalid_handler_message(
        self, mock_client: MagicMock, mock_join_community: MagicMock
    ):
        """Test method for handle_message with invalid MessageDataclass."""
        invalid_message = MessageDataclass(header="INVALID_HEADER", content="content")
        message_handler = MessageHandler(mock_join_community)

        with pytest.raises(MessageError):
            message_handler.handle_message(mock_client, invalid_message)
