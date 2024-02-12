from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.imessage_formatter import IMessageFormatter
from src.application.interfaces.iparent_connection import IParentConnection
from src.domain.entities.member import Member
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader
import src.presentation.network.client as client


class ParentConnection(IParentConnection):
    """Manager for parent connection."""

    def __init__(
        self,
        member_repository: IMemberRepository,
        message_formatter: IMessageFormatter,
        machine_service: IMachineService,
    ):
        self.member_repository = member_repository
        self.message_formatter = message_formatter
        self.machine_service = machine_service

    def execute(
        self, community_id: str, old_parent_auth_key: str | None = None
    ) -> Member | None:
        author = self.machine_service.get_current_user(community_id)
        members = self.member_repository.get_older_members_from_community(
            community_id, author.creation_date
        )
        members = list(
            filter(
                lambda member: member.authentication_key != old_parent_auth_key, members
            )
        )

        message = MessageDataclass(
            MessageHeader.REQUEST_PARENT,
            author.authentication_key,
            community_id,
        )

        parent_found: Member = None
        for member in reversed(members):
            client_socket: client.Client = None
            try:
                client_socket = client.Client(self.message_formatter)
                client_socket.connect_to_server(member.ip_address, member.port)
                client_socket.send_message(message)

                received_message, _ = client_socket.receive_message()
                if received_message and received_message.header == MessageHeader.ACCEPT:
                    self.member_repository.update_member_relationship(
                        community_id, member.authentication_key, "parent"
                    )
                    parent_found = member
                    break
            except:
                pass
            finally:
                if client_socket is not None:
                    client_socket.close_connection()

        return parent_found

    def response(self, client: client.Client, community_id: str, auth_key: str) -> str:
        try:
            self.member_repository.update_member_relationship(
                community_id, auth_key, "child"
            )
            client.send_message(MessageDataclass(MessageHeader.ACCEPT))
            return "Success!"
        except Exception as error:
            client.send_message(MessageDataclass(MessageHeader.REJECT))
            return str(error)
        finally:
            client.close_connection()
