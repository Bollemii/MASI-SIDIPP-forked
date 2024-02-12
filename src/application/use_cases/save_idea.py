from src.application.interfaces.icommunity_service import ICommunityService
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.isave_idea import ISaveIdea
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.domain.entities.idea import Idea


class SaveIdea(ISaveIdea):
    """Save an idea."""

    def __init__(
        self,
        idea_repository: IIdeaRepository,
        symetric_encryption_service: ISymetricEncryptionService,
        community_service: ICommunityService,
    ):
        self.idea_repository = idea_repository
        self.symetric_encryption_service = symetric_encryption_service
        self.community_service = community_service

    def execute(self, community_id: str, message: str) -> str:
        try:
            nonce, tag, cipher_idea = message.split(",", maxsplit=2)

            symetric_key = self.community_service.get_community_symetric_key(
                community_id
            )
            decrypted_idea = self.symetric_encryption_service.decrypt(
                cipher_idea, symetric_key, tag, nonce
            )

            idea = Idea.from_str(decrypted_idea)
            if not self.community_service.is_community_member(
                community_id, idea.author.authentication_key
            ):
                raise ValueError("Author is not a member of the community.")
            if len(idea.content) < Idea.CONTENT_MIN_LENGTH:
                raise ValueError("Content is too short.")

            self.idea_repository.add_idea_to_community(community_id, idea)
            return "Success!"
        except Exception as error:
            return str(error)
