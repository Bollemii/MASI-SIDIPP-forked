from src.application.interfaces.iarchitecture_manager import IArchitectureManager
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.imessage_formatter import IMessageFormatter
from src.presentation.formatting.message_dataclass import MessageDataclass
import src.presentation.network.client as client


class ArchitectureManager(IArchitectureManager):
    """Manager for communities architecture."""

    def __init__(
        self,
        member_repository: IMemberRepository,
        message_formatter: IMessageFormatter,
        machine_service: IMachineService,
    ):
        self.member_repository = member_repository
        self.message_formatter = message_formatter
        self.machine_service = machine_service

    def share(
        self,
        message: MessageDataclass,
        community_id: str,
        excluded_auth_keys: list[str] = [],
        excluded_ip_addresses: list[str] = [],
    ):
        author = self.machine_service.get_current_user(community_id)
        excluded_auth_keys.append(author.authentication_key)
        excluded_ip_addresses.append(author.ip_address)
        members = filter(
            lambda member: member.authentication_key not in excluded_auth_keys
            and member.ip_address not in excluded_ip_addresses,
            self.member_repository.get_members_from_community(
                community_id, is_related=True
            ),
        )
        for member in members:
            client_socket: client.Client = None
            try:
                client_socket = client.Client(self.message_formatter)
                client_socket.connect_to_server(member.ip_address, member.port)
                client_socket.send_message(message)
            except:
                pass
            finally:
                if client_socket is not None:
                    client_socket.close_connection()
