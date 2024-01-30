from src.application.interfaces.icreate_idea import ICreateIdea
from src.application.interfaces.idatetime_service import IDatetimeService
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.domain.entities.idea import Idea
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
from src.presentation.manager.architecture_manager import ArchitectureManager
from src.presentation.manager.community_manager import CommunityManager


class CreateIdea(ICreateIdea):
    """Create an idea."""

    def __init__(
        self,
        machine_service: IMachineService,
        id_generator_service: IIdGeneratorService,
        idea_repository: IIdeaRepository,
        symetric_encryption_service: ISymetricEncryptionService,
        datetime_service: IDatetimeService,
        community_manager: CommunityManager,
        architecture_manager: ArchitectureManager,
    ):
        self.machine_service = machine_service
        self.id_generator_service = id_generator_service
        self.idea_repository = idea_repository
        self.symetric_encryption_service = symetric_encryption_service
        self.datetime_service = datetime_service
        self.community_manager = community_manager
        self.architecture_manager = architecture_manager

    def execute(self, community_id: str, content: str) -> str:
        """Create an idea."""
        try:
            symetric_key = self.community_manager.get_community_symetric_key(
                community_id
            )
            author = self.machine_service.get_current_user(community_id)

            idea = Idea(
                self.id_generator_service.generate(),
                content,
                author,
                self.datetime_service.get_datetime(),
            )
            self.idea_repository.add_idea_to_community(community_id, idea)

            (nonce, tag, cipher) = self.symetric_encryption_service.encrypt(
                idea.to_str(), symetric_key
            )
            message_dataclass = MessageDataclass(
                MessageHeader.CREATE_IDEA,
                f"{nonce},{tag},{cipher}",
                community_id,
            )
            self.architecture_manager.share(message_dataclass, community_id)

            return "Success!"
        except Exception as error:
            return str(error)
