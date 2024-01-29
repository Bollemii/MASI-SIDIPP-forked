import pytest

from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.presentation.formatting.message_formatter import MessageFormatter
from src.application.exceptions.message_error import MessageError


class TestMessageFormatter:
    """the test message formatter class"""

    @pytest.fixture(scope="function", autouse=True, name="message")
    def create_message(self) -> MessageDataclass:
        """Fixture to create a MessageDataclass with different MessageHeader."""
        header = MessageHeader.INVITATION
        content = "content"
        return MessageDataclass(header=header, content=content)

    @pytest.fixture(scope="function", autouse=True, name="formatter")
    def create_formatter(self) -> MessageFormatter:
        """Fixture to create a default Formatter for testing."""
        return MessageFormatter()

    def test_format_message(
        self, formatter: MessageFormatter, message: MessageDataclass
    ):
        """Test that the formatter formats the message to a string"""
        formated_message = formatter.format(message)
        expected_message = f"{message.header}|{message.content}"
        assert formated_message == expected_message

    def test_invalid_format_message(self, formatter: MessageFormatter):
        """Test that the formatter raises an error when the message header is invalid"""
        invalid_message_data = MessageDataclass(
            header="INVALID_HEADER", content="content"
        )
        with pytest.raises(MessageError):
            formatter.format(invalid_message_data)

    def test_format_message_with_community_id(
        self, formatter: MessageFormatter, message: MessageDataclass
    ):
        """Test that the formatter formats the message to a string with community id"""
        message.community_id = "community_id"
        formated_message = formatter.format(message)
        expected_message = f"{message.header}|{message.community_id}|{message.content}"
        assert formated_message == expected_message

    def test_parse_invitation_string_message(self, formatter: MessageFormatter):
        """Test that the formatter parses the string to a message object"""
        formated_data = "INVITATION|content"
        parsed_message = formatter.parse(formated_data)

        assert parsed_message.header == MessageHeader.INVITATION
        assert parsed_message.content == "content"

    def test_parse_invalid_message(self, formatter: MessageFormatter):
        """Test that the formatter raises an error when the message is invalid"""
        formated_data = "content"
        with pytest.raises(MessageError):
            formatter.parse(formated_data)

    def test_parse_invalid_message_header(self, formatter: MessageFormatter):
        """Test that the formatter raises an error when the message header is invalid"""
        formated_data = "INVALID_HEADER|content"
        with pytest.raises(MessageError):
            formatter.parse(formated_data)

    def test_parse_message_with_community_id(self, formatter: MessageFormatter):
        """Test that the formatter parses the string to a message object with community id"""
        formated_data = "INVITATION|community_id|content"
        parsed_message = formatter.parse(formated_data)

        assert parsed_message.header == MessageHeader.INVITATION
        assert parsed_message.community_id == "community_id"
        assert parsed_message.content == "content"
