from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.icreate_opinion import ICreateOpinion
from src.application.interfaces.idatetime_service import IDatetimeService
from src.application.interfaces.ifile_service import IFileService
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.imessage_formatter import IMessageFormatter
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.domain.entities.opinion import Opinion
from src.domain.exceptions.parent_not_found_error import ParentNotFoundError
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.presentation.manager.community_manager import CommunityManager
from src.presentation.network import client


class CreateOpinion(ICreateOpinion):
    """Create an opinion."""

    def __init__(
        self,
        machine_service: IMachineService,
        id_generator_service: IIdGeneratorService,
        idea_repository: IIdeaRepository,
        opinion_repository: IOpinionRepository,
        member_repository: IMemberRepository,
        community_repository: ICommunityRepository,
        symetric_encryption_service: ISymetricEncryptionService,
        file_service: IFileService,
        datetime_service: IDatetimeService,
        message_formatter: IMessageFormatter,
        community_manager: CommunityManager,
    ):
        self.machine_service = machine_service
        self.id_generator_service = id_generator_service
        self.idea_repository = idea_repository
        self.opinion_repository = opinion_repository
        self.member_repository = member_repository
        self.community_repository = community_repository
        self.symetric_encryption_service = symetric_encryption_service
        self.file_service = file_service
        self.datetime_service = datetime_service
        self.message_formatter = message_formatter
        self.community_manager = community_manager

    def execute(self, community_id: str, idea_or_opinion_id: str, content: str) -> str:
        try:
            symetric_key = self.community_manager.get_community_symetric_key(
                community_id
            )
            author = self.machine_service.get_current_user(community_id)
            members = filter(
                lambda member: member.authentication_key != author.authentication_key,
                self.member_repository.get_members_from_community(community_id),
            )

            parent = self.idea_repository.get_idea_from_community(
                community_id, idea_or_opinion_id
            ) or self.opinion_repository.get_opinion_from_community(
                community_id, idea_or_opinion_id
            )

            if parent is None:
                raise ParentNotFoundError()

            opinion = Opinion(
                self.id_generator_service.generate(),
                content,
                author,
                self.datetime_service.get_datetime(),
                parent,
            )
            self.opinion_repository.add_opinion_to_community(community_id, opinion)

            (nonce, tag, cipher) = self.symetric_encryption_service.encrypt(
                opinion.to_str(), symetric_key
            )
            message_dataclass = MessageDataclass(
                MessageHeader.CREATE_OPINION,
                f"{nonce},{tag},{cipher}",
                community_id,
            )

            for member in members:
                client_socket: client.Client = None
                try:
                    client_socket = client.Client(self.message_formatter)
                    client_socket.connect_to_server(member.ip_address, member.port)
                    client_socket.send_message(message_dataclass)
                except:
                    pass
                finally:
                    if client_socket is not None:
                        client_socket.close_connection()
            return "Success!"
        except Exception as error:
            return str(error)
