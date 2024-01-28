import socket
from src.application.exceptions.message_error import MessageError

from src.application.exceptions.socket_error import SocketError
from src.application.interfaces.iserver_socket import IServerSocket
from src.presentation.formatting.message_dataclass import MessageDataclass
import src.presentation.network.client as client
from src.application.interfaces.imessage_handler import IMessageHandler
from src.application.interfaces.imessage_formatter import IMessageFormatter


class Server(IServerSocket):
    """Server class"""

    def __init__(
        self,
        port: int,
        message_handler: IMessageHandler,
        message_formatter: IMessageFormatter,
    ):
        super().__init__()
        self.port = port
        self.message_handler = message_handler
        self.message_formatter = message_formatter

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.running = False
        except socket.error as err:
            raise SocketError(f"Unable to create socket :{err}") from err

    def run(self):
        try:
            self.server_socket.settimeout(1)
            self.server_socket.bind(("", self.port))
            self.server_socket.listen(5)
        except socket.error as err:
            raise SocketError(f"Unable to run server :{err}") from err

        self.running = True
        while self._is_running():
            try:
                client_socket, _ = self.server_socket.accept()
                client_socket = client.Client(self.message_formatter, client_socket)
                message, _ = client_socket.receive_message()
                if not isinstance(message, MessageDataclass):
                    raise MessageError(f"Invalid received message : {message}")
                self.message_handler.handle_message(client_socket, message)

                client_socket.close_connection()
            except socket.timeout:
                pass
            except MessageError as err:
                print(err)

        self.server_socket.close()

    def _is_running(self) -> bool:
        """Returns if the server is running"""
        return self.running

    def stop(self):
        self.running = False
