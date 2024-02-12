from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.ideconnection import IDeconnection
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.iparent_connection import IParentConnection
from src.application.interfaces.ishare_information import IShareInformation
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader


class Deconnection(IDeconnection):
    """Deconnection of all communities"""

    def __init__(
        self,
        community_repository: ICommunityRepository,
        machine_service: IMachineService,
        member_repository: IMemberRepository,
        share_information: IShareInformation,
        parent_connection: IParentConnection,
    ):
        self.community_repository = community_repository
        self.machine_service = machine_service
        self.member_repository = member_repository
        self.share_information = share_information
        self.parent_connection = parent_connection

    def execute(self):
        communities = self.community_repository.get_communities()

        for community in communities:
            author = self.machine_service.get_current_user(community.identifier)
            message = MessageDataclass(
                MessageHeader.DECONNECTION,
                author.authentication_key,
                community.identifier,
            )
            self.share_information.execute(message, community.identifier)

            self.member_repository.clear_members_relationship(community.identifier)

    def deconnect_member(self, community_id: str, auth_key: str):
        member = self.member_repository.get_member_for_community(community_id, auth_key)

        self.member_repository.update_member_relationship(
            community_id, auth_key, relationship=None
        )
        if member.relationship == "parent":
            self.parent_connection.execute(community_id, auth_key)
