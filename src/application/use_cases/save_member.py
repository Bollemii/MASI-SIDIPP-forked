from src.application.interfaces.icommunity_manager import ICommunityManager
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.isave_member import ISaveMember
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.domain.entities.member import Member


class SaveMember(ISaveMember):
    """Use case for saving a member."""

    def __init__(
        self,
        member_repository: IMemberRepository,
        community_manager: ICommunityManager,
        symetric_encryption_service: ISymetricEncryptionService,
    ):
        self.member_repository = member_repository
        self.community_manager = community_manager
        self.symetric_encryption_service = symetric_encryption_service

    def execute(self, community_id: str, message: str) -> str:
        try:
            nonce, tag, cipher_member = message.split(",", maxsplit=2)

            symetric_key = self.community_manager.get_community_symetric_key(
                community_id
            )
            decrypted_member = self.symetric_encryption_service.decrypt(
                cipher_member, symetric_key, tag, nonce
            )

            member = Member.from_str(decrypted_member)

            self.member_repository.add_member_to_community(community_id, member)
            return "Success!"
        except Exception as error:
            return str(error)
