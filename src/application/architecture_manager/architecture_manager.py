from src.application.interfaces.iarchitecture_manager import IArchitectureManager
from src.domain.entities.member import Member
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.application.interfaces.ishare_information import IShareInformation
from src.application.architecture_manager.parent_connection import ParentConnection


class ArchitectureManager(IArchitectureManager):
    """Manager for communities architecture."""

    def __init__(
        self,
        share_information_usecase: IShareInformation,
        parent_connection: ParentConnection,
    ):
        self.share_information_usecase = share_information_usecase
        self.parent_connection_usecase = parent_connection

    def share_information(
        self,
        message: MessageDataclass,
        community_id: str,
        excluded_auth_keys: list[str] = [],
        excluded_ip_addresses: list[str] = [],
    ):
        self.share_information_usecase.execute(
            message, community_id, excluded_auth_keys, excluded_ip_addresses
        )

    def connect_to_parent(self, community_id: str) -> Member | None:
        return self.parent_connection_usecase.execute(community_id)
