from src.application.interfaces.imessage_formatter import IMessageFormatter
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_dataclass import MessageHeader
from src.application.exceptions.message_error import MessageError


class MessageFormatter(IMessageFormatter):
    """Class to format and parse message objects"""

    def format(self, message: MessageDataclass) -> str:
        if message.header in MessageHeader.__members__:
            if message.community_id is None:
                return f"{message.header}|{message.content}"
            else:
                return f"{message.header}|{message.community_id}|{message.content}"
        else:
            raise MessageError("Invalid message header")

    def parse(self, formated_message: str) -> MessageDataclass:
        try:
            header, content = formated_message.split("|", 1)
            if header not in MessageHeader.__members__:
                raise ValueError("Invalid message header")

            try:
                community_id, content = content.split("|", 1)
            except ValueError:
                community_id = None

            return MessageDataclass(header, content, community_id)
        except ValueError as err:
            raise MessageError(f"Invalid message format :{err}") from err
