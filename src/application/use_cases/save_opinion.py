from src.application.interfaces.icommunity_manager import ICommunityManager
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.application.interfaces.isave_opinion import ISaveOpinion
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.domain.entities.opinion import Opinion


class SaveOpinion(ISaveOpinion):
    """Save an opinion."""

    def __init__(
        self,
        opinion_repository: IOpinionRepository,
        symetric_encryption_service: ISymetricEncryptionService,
        community_manager: ICommunityManager,
    ):
        self.opinion_repository = opinion_repository
        self.symetric_encryption_service = symetric_encryption_service
        self.community_manager = community_manager

    def execute(self, community_id: str, message: str) -> str:
        try:
            nonce, tag, cipher_opinion = message.split(",", maxsplit=2)

            symetric_key = self.community_manager.get_community_symetric_key(
                community_id
            )
            decrypted_opinion = self.symetric_encryption_service.decrypt(
                cipher_opinion, symetric_key, tag, nonce
            )

            opinion = Opinion.from_str(decrypted_opinion)
            if not self.community_manager.is_community_member(
                community_id, opinion.author.authentication_key
            ):
                raise ValueError("Author is not a member of the community.")
            if len(opinion.content) < Opinion.CONTENT_MIN_LENGTH:
                raise ValueError("Content is too short.")

            self.opinion_repository.add_opinion_to_community(community_id, opinion)
            return "Success!"
        except Exception as error:
            return str(error)
