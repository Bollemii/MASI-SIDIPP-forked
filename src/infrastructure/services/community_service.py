from src.application.interfaces.icommunity_service import ICommunityService
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.ifile_service import IFileService
from src.application.interfaces.imember_repository import IMemberRepository


class CommunityService(ICommunityService):
    """Manager for Community"""

    def __init__(
        self,
        community_repository: ICommunityRepository,
        member_repository: IMemberRepository,
        file_service: IFileService,
    ):
        self.community_repository = community_repository
        self.member_repository = member_repository
        self.file_service = file_service

    def get_community_symetric_key(self, community_id: str) -> str:
        symetric_key_path = self.community_repository.get_community_encryption_key_path(
            community_id
        )
        return self.file_service.read_file(symetric_key_path)

    def is_community_member(
        self,
        community_id: str,
        auth_key: str | None = None,
        ip_address: str | None = None,
    ) -> bool:
        member = self.member_repository.get_member_for_community(
            community_id, auth_key, ip_address
        )
        return member is not None
