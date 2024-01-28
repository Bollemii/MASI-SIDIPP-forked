import socket
from src.application.exceptions.message_error import MessageError

from src.application.exceptions.socket_error import SocketError
from src.application.interfaces.iclient_socket import IClientSocket
from src.application.interfaces.imessage_formatter import IMessageFormatter
from src.presentation.formatting.message_dataclass import MessageDataclass


class Client(IClientSocket):
    "Client socket class"
    BUFFER_SIZE = 2048

    def __init__(
        self, message_formatter: IMessageFormatter, client_socket: socket.socket = None
    ):
        self.message_formatter = message_formatter
        try:
            if client_socket is not None:
                self.client_socket = client_socket
            else:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            raise SocketError(f"Unable to create socket :{err}") from err

    def connect_to_server(self, ip_adress: str, port: int):
        try:
            self.client_socket.connect((ip_adress, port))
        except socket.error as err:
            raise SocketError(f"Unable to connect to server :{err}") from err

    def send_message(
        self,
        message: str | MessageDataclass,
        ip_address: str | None = None,
        port: int | None = None,
    ):
        has_target_data = ip_address is not None and port is not None
        if isinstance(message, MessageDataclass):
            message_to_send = self.message_formatter.format(message)
        else:
            message_to_send = message
        try:
            while len(message_to_send) > 0:
                encoded_chunk = message_to_send[: Client.BUFFER_SIZE].encode()
                if has_target_data:
                    self.client_socket.sendto(encoded_chunk, (ip_address, port))
                else:
                    self.client_socket.send(encoded_chunk)
                message_to_send = message_to_send[Client.BUFFER_SIZE :]
        except socket.error as err:
            raise SocketError(f"Unable to send message :{err}") from err

    def receive_message(
        self,
    ) -> tuple[str, tuple[str, int]] | tuple[MessageDataclass, tuple[str, int]]:
        message, sender = self.client_socket.recvfrom(Client.BUFFER_SIZE)
        decoded_message = message.decode()
        if len(message) == Client.BUFFER_SIZE:
            while message:
                message, _ = self.client_socket.recvfrom(Client.BUFFER_SIZE)
                decoded_message = decoded_message + message.decode()

        try:
            decoded_message = self.message_formatter.parse(decoded_message)
        except MessageError:
            pass

        return decoded_message, sender

    def close_connection(self):
        self.client_socket.close()
