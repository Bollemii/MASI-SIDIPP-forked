from src.application.interfaces.idatetime_service import IDatetimeService
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.icreate_community import ICreateCommunity
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.application.interfaces.ifile_service import IFileService
from src.domain.entities.community import Community
from src.domain.entities.member import Member


class CreateCommunity(ICreateCommunity):
    """Class to create a community"""

    def __init__(
        self,
        keys_folder_path: str,
        community_repository: ICommunityRepository,
        member_repository: IMemberRepository,
        idea_repository: IIdeaRepository,
        opinion_repository: IOpinionRepository,
        id_generator_service: IIdGeneratorService,
        encryption_service: ISymetricEncryptionService,
        machine_service: IMachineService,
        file_service: IFileService,
        datetime_service: IDatetimeService,
    ):
        self.keys_folder_path = keys_folder_path
        self.community_repository = community_repository
        self.member_repository = member_repository
        self.idea_repository = idea_repository
        self.opinion_repository = opinion_repository
        self.id_generator_service = id_generator_service
        self.encryption_service = encryption_service
        self.machine_service = machine_service
        self.file_service = file_service
        self.datetime_service = datetime_service

    def execute(self, name: str, description: str) -> str:
        try:
            if len(name) < Community.NAME_MIN_LENGTH:
                raise ValueError(
                    f"Name must be at least {Community.NAME_MIN_LENGTH} characters long."
                )

            member = self._create_member()
            community = self._create_community(name, description, member)

            encryption_key_path = self._generate_community_key(community.identifier)

            self.community_repository.add_community(
                community, member.authentication_key, encryption_key_path
            )

            self._initialize_community_database(community.identifier)
            self._add_member_to_community(community.identifier, member)

            return "Success!"
        except Exception as error:
            return str(error)

    def _create_member(self) -> Member:
        """Creates a member with the current user"""
        return self.machine_service.get_current_user()

    def _create_community(
        self, name: str, description: str, member: Member
    ) -> Community:
        """Creates a community with the given parameters"""
        community = Community(
            self.id_generator_service.generate(),
            name,
            description,
            self.datetime_service.get_datetime(),
        )
        community.add_member(member)
        return community

    def _generate_community_key(self, community_id: str) -> str:
        """Generates a encryption key for the community"""
        key = self.encryption_service.generate_key()
        encryption_key_path = f"{self.keys_folder_path}/{community_id}.key"
        self.file_service.write_file(encryption_key_path, key)
        return encryption_key_path

    def _initialize_community_database(self, community_id: str) -> None:
        """Initializes the database for the community"""
        self.member_repository.initialize_if_not_exists(community_id)
        self.idea_repository.initialize_if_not_exists(community_id)
        self.opinion_repository.initialize_if_not_exists(community_id)

    def _add_member_to_community(self, community_id: str, member: Member) -> None:
        """Adds the current user as a member to the community"""
        self.member_repository.add_member_to_community(community_id, member)
