from src.application.interfaces.imessage_handler import IMessageHandler
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.application.exceptions.message_error import MessageError
from src.application.interfaces.ijoin_community import IJoinCommunity
from src.presentation.network.client import Client


class MessageHandler(IMessageHandler):
    """Class to execute an action based on the message"""

    def __init__(self, join_community_usecase: IJoinCommunity):
        self.join_community_usecase = join_community_usecase

    def handle_message(self, client: Client, message: MessageDataclass):
        match message.header:
            case MessageHeader.INVITATION:
                self.join_community_usecase.execute(client)
            case MessageHeader.CREATE_IDEA:
                print(f"Received idea : {message.content}")
            case MessageHeader.CREATE_OPINION:
                print(f"Received opinion : {message.content}")
            case _:
                raise MessageError("Invalid header in the message.")
