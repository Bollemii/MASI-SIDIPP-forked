from src.application.interfaces.iarchitecture_manager import IArchitectureManager
from src.application.interfaces.icreate_opinion import ICreateOpinion
from src.application.interfaces.idatetime_service import IDatetimeService
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.domain.entities.opinion import Opinion
from src.domain.exceptions.parent_not_found_error import ParentNotFoundError
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.presentation.manager.community_manager import CommunityManager


class CreateOpinion(ICreateOpinion):
    """Create an opinion."""

    def __init__(
        self,
        machine_service: IMachineService,
        id_generator_service: IIdGeneratorService,
        idea_repository: IIdeaRepository,
        opinion_repository: IOpinionRepository,
        symetric_encryption_service: ISymetricEncryptionService,
        datetime_service: IDatetimeService,
        community_manager: CommunityManager,
        architecture_manager: IArchitectureManager,
    ):
        self.machine_service = machine_service
        self.id_generator_service = id_generator_service
        self.idea_repository = idea_repository
        self.opinion_repository = opinion_repository
        self.symetric_encryption_service = symetric_encryption_service
        self.datetime_service = datetime_service
        self.community_manager = community_manager
        self.architecture_manager = architecture_manager

    def execute(self, community_id: str, idea_or_opinion_id: str, content: str) -> str:
        try:
            symetric_key = self.community_manager.get_community_symetric_key(
                community_id
            )
            author = self.machine_service.get_current_user(community_id)

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
            self.architecture_manager.share(message_dataclass, community_id)

            return "Success!"
        except Exception as error:
            return str(error)
