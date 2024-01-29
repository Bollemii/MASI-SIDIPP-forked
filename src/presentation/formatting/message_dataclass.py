from dataclasses import dataclass

from src.presentation.formatting.message_header import MessageHeader


@dataclass
class MessageDataclass:
    """Class to represent a message object"""

    header: MessageHeader
    content: str | None = None
    community_id: str | None = None
