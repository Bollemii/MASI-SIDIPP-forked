import os
import threading
from src.application.use_cases.save_member import SaveMember

from src.infrastructure.repositories.community_repository import CommunityRepository
from src.infrastructure.repositories.member_repository import MemberRepository
from src.infrastructure.repositories.idea_repository import IdeaRepository
from src.infrastructure.repositories.opinion_repository import OpinionRepository
from src.infrastructure.services.ntp_datetime_service import NtpDatetimeService
from src.infrastructure.services.uuid_generator_service import UuidGeneratorService
from src.infrastructure.services.machine_service import MachineService
from src.infrastructure.services.asymetric_encryption_service import (
    AsymetricEncryptionService,
)
from src.infrastructure.services.symetric_encryption_service import (
    SymetricEncryptionService,
)
from src.infrastructure.services.file_service import FileService
from src.application.use_cases.create_community import CreateCommunity
from src.application.use_cases.add_member import AddMember
from src.application.use_cases.join_community import JoinCommunity
from src.application.use_cases.read_communities import ReadCommunities
from src.application.use_cases.read_ideas_from_community import ReadIdeasFromCommunity
from src.application.use_cases.read_opinions import ReadOpinions
from src.application.use_cases.create_idea import CreateIdea
from src.application.use_cases.create_opinion import CreateOpinion
from src.application.use_cases.save_idea import SaveIdea
from src.application.use_cases.save_opinion import SaveOpinion
from src.presentation.formatting.message_formatter import MessageFormatter
from src.presentation.handler.message_handler import MessageHandler
from src.presentation.manager.architecture_manager import ArchitectureManager
from src.presentation.manager.community_manager import CommunityManager
from src.presentation.network.server import Server
from src.presentation.views.menus.main_menu import MainMenu


class Application:
    """The application's entry point."""

    stopped: bool = False
    threads: list[threading.Thread] = []

    def __init__(self):
        base_path = os.path.join(os.getcwd(), "data")
        os.makedirs(base_path, exist_ok=True)
        keys_path = os.path.join(base_path, "keys")
        os.makedirs(keys_path, exist_ok=True)

        self.community_repository = CommunityRepository(base_path)
        self.member_repository = MemberRepository(base_path)
        self.idea_repository = IdeaRepository(base_path)
        self.opinion_repository = OpinionRepository(base_path)

        self.message_formatter = MessageFormatter()

        self.datetime_service = NtpDatetimeService()
        self.id_generator = UuidGeneratorService()
        self.file_service = FileService()
        self.asymetric_encryption_service = AsymetricEncryptionService()
        self.symetric_encryption_service = SymetricEncryptionService()
        self.machine_service = MachineService(
            base_path,
            self.community_repository,
            self.id_generator,
            self.asymetric_encryption_service,
            self.file_service,
            self.datetime_service,
        )

        self.community_manager = CommunityManager(
            self.community_repository, self.member_repository, self.file_service
        )
        self.architecture_manager = ArchitectureManager(
            self.member_repository, self.message_formatter, self.machine_service
        )

        self.create_community_usecase = CreateCommunity(
            keys_path,
            self.community_repository,
            self.member_repository,
            self.idea_repository,
            self.opinion_repository,
            self.id_generator,
            self.symetric_encryption_service,
            self.machine_service,
            self.file_service,
            self.datetime_service,
        )
        self.add_member_usecase = AddMember(
            base_path,
            self.id_generator,
            self.asymetric_encryption_service,
            self.symetric_encryption_service,
            self.machine_service,
            self.file_service,
            self.community_repository,
            self.member_repository,
            self.datetime_service,
            self.message_formatter,
            self.community_manager,
            self.architecture_manager,
        )
        self.join_community_usecase = JoinCommunity(
            base_path,
            keys_path,
            self.symetric_encryption_service,
            self.asymetric_encryption_service,
            self.machine_service,
            self.file_service,
            self.community_repository,
        )
        self.read_communities_usecase = ReadCommunities(self.community_repository)
        self.read_ideas_from_community_usecase = ReadIdeasFromCommunity(
            self.idea_repository
        )
        self.read_opinions_usecase = ReadOpinions(self.opinion_repository)
        self.create_idea_usecase = CreateIdea(
            self.machine_service,
            self.id_generator,
            self.idea_repository,
            self.symetric_encryption_service,
            self.datetime_service,
            self.community_manager,
            self.architecture_manager,
        )
        self.create_opinion_usecase = CreateOpinion(
            self.machine_service,
            self.id_generator,
            self.idea_repository,
            self.opinion_repository,
            self.symetric_encryption_service,
            self.datetime_service,
            self.community_manager,
            self.architecture_manager,
        )
        self.save_member_usecase = SaveMember(
            self.member_repository,
            self.community_manager,
            self.symetric_encryption_service,
        )
        self.save_idea_usecase = SaveIdea(
            self.idea_repository,
            self.symetric_encryption_service,
            self.community_manager,
        )
        self.save_opinion_usecase = SaveOpinion(
            self.opinion_repository,
            self.symetric_encryption_service,
            self.community_manager,
        )

        self.message_handler = MessageHandler(
            self.community_manager,
            self.join_community_usecase,
            self.save_member_usecase,
            self.save_idea_usecase,
            self.save_opinion_usecase,
        )

        self.server_socket = Server(
            self.machine_service.get_port(),
            self.message_handler,
            self.message_formatter,
        )

    def run(self):
        """Configures the dependencies and runs the application."""
        server_thread = threading.Thread(target=self.server_socket.run, daemon=True)
        self.threads.append(server_thread)
        server_thread.start()

        gen_keys_thread = threading.Thread(
            target=self.machine_service.get_asymetric_key_pair
        )
        self.threads.append(gen_keys_thread)
        gen_keys_thread.start()

        MainMenu(
            self.create_community_usecase,
            self.add_member_usecase,
            self.read_communities_usecase,
            self.read_ideas_from_community_usecase,
            self.read_opinions_usecase,
            self.create_idea_usecase,
            self.create_opinion_usecase,
            self.machine_service,
        ).show()

    def stop(self):
        """Stops the application."""
        if not self.stopped:
            self.stopped = True
            self.server_socket.stop()
            for thread in self.threads:
                if thread.is_alive():
                    thread.join()
