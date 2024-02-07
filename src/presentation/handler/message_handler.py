from src.application.interfaces.iarchitecture_manager import IArchitectureManager
from src.application.interfaces.icommunity_manager import ICommunityManager
from src.application.interfaces.imessage_handler import IMessageHandler
from src.application.interfaces.isave_idea import ISaveIdea
from src.application.interfaces.isave_member import ISaveMember
from src.application.interfaces.isave_opinion import ISaveOpinion
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.application.exceptions.message_error import MessageError
from src.application.interfaces.ijoin_community import IJoinCommunity
from src.presentation.network.client import Client


class MessageHandler(IMessageHandler):
    """Class to execute an action based on the message"""

    def __init__(
        self,
        community_manager: ICommunityManager,
        architecture_manager: IArchitectureManager,
        join_community_usecase: IJoinCommunity,
        save_member_usecase: ISaveMember,
        save_idea_usecase: ISaveIdea,
        save_opinion_usecase: ISaveOpinion,
    ):
        self.community_manager = community_manager
        self.architecture_manager = architecture_manager
        self.join_community_usecase = join_community_usecase
        self.save_member_usecase = save_member_usecase
        self.save_idea_usecase = save_idea_usecase
        self.save_opinion_usecase = save_opinion_usecase

    def handle_message(
        self, sender: tuple[str, int], client: Client, message: MessageDataclass
    ):
        if message.header != MessageHeader.INVITATION:
            if not self.community_manager.is_community_member(
                message.community_id, ip_address=sender[0]
            ):
                raise MessageError("User is not a member of the community.")

        match message.header:
            case MessageHeader.INVITATION:
                self.join_community_usecase.execute(client)
            case MessageHeader.ADD_MEMBER:
                self.save_member_usecase.execute(message.community_id, message.content)
            case MessageHeader.CREATE_IDEA:
                self.save_idea_usecase.execute(message.community_id, message.content)
            case MessageHeader.CREATE_OPINION:
                self.save_opinion_usecase.execute(message.community_id, message.content)
            case _:
                raise MessageError("Invalid header in the message.")

        if message.header != MessageHeader.INVITATION:
            self.architecture_manager.share(
                message, message.community_id, excluded_ip_addresses=[sender[0]]
            )
