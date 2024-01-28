from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader


class TestMessageDataclass:
    """The test message dataclass"""

    def test_message_dataclass_creation(self):
        """Test that the message dataclass is created"""
        header = MessageHeader.INVITATION
        content = "content"

        message_data = MessageDataclass(header, content)

        assert message_data.header == header
        assert message_data.content == content
