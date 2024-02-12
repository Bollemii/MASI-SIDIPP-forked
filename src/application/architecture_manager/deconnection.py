from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.ideconnection import IDeconnection
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.ishare_information import IShareInformation
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader


class Deconnection(IDeconnection):
    """Deconnection of all communities"""

    def __init__(
        self,
        community_repository: ICommunityRepository,
        member_repository: IMemberRepository,
        share_information: IShareInformation,
    ):
        self.community_repository = community_repository
        self.member_repository = member_repository
        self.share_information = share_information

    def execute(self):
        communities = self.community_repository.get_communities()

        for community in communities:
            message = MessageDataclass(
                MessageHeader.DECONNECTION, community_id=community.identifier
            )
            self.share_information.execute(message, community.identifier)

            self.member_repository.clear_members_relationship(community.identifier)
