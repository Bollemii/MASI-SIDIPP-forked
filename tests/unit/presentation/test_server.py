from unittest import mock
from unittest.mock import MagicMock
import pytest
from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_header import MessageHeader

from src.presentation.network.server import Server
from src.presentation.network.client import Client


class TestServer:
    """Test Server class"""

    @pytest.fixture(scope="function", autouse=True, name="server")
    @mock.patch("socket.socket")
    @mock.patch("src.application.interfaces.imessage_handler", name="message_handler")
    @mock.patch(
        "src.application.interfaces.imessage_formatter", name="message_formatter"
    )
    def create_server(
        self,
        mock_socket: MagicMock,  # pylint: disable=unused-argument
        message_formatter: MagicMock,
        message_handler: MagicMock,
    ) -> Server:
        """Create the server"""
        server = Server(1234, message_handler, message_formatter)

        server.server_socket.accept.side_effect = TimeoutError()

        return server

    def test_init(self, server: Server):
        """Validates the constructor of Server initializes the object"""
        assert server is not None

    def test_port_attribute(self, server: Server):
        """Validates the attribute port of the server"""
        port = 1234

        assert server.port == port

    def test_server_socket_created(self, server: Server):
        """Validates that the server socket is created"""

        assert server.server_socket is not None

    def test_stop_server_running(self, server: Server):
        """Test stop server"""
        server.running = True
        server.stop()

        assert not server.running

    def test_stop_server_socket(self, server: Server):
        """Test stop server"""
        server.running = True
        server.stop()

        assert not server.running

    def test_server_running(self, server: Server):
        """Test server running call bind"""
        mock_running = MagicMock()
        mock_running.return_value = False
        server._is_running = mock_running  # pylint: disable=protected-access

        server.run()

        server.server_socket.bind.assert_called_once()

    def test_server_running_accept(self, server: Server):
        """Test server running call accept"""
        mock_running = MagicMock()
        mock_running.side_effect = [True, False]
        server._is_running = mock_running  # pylint: disable=protected-access

        server.run()

        server.server_socket.accept.assert_called()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_server_running_receive_message(self, mock_client: Client, server: Server):
        """Test server running call accept"""
        mock_running = MagicMock()
        mock_running.side_effect = [True, False]
        server._is_running = mock_running  # pylint: disable=protected-access

        server.server_socket.accept.side_effect = None
        server.server_socket.accept.return_value = (mock_client, None)

        mock_client.return_value = mock_client
        mock_client.receive_message.return_value = (
            MessageDataclass(MessageHeader.DATA, "test"),
            None,
        )

        server.run()

        server.message_handler.handle_message.assert_called_once()
        mock_client.close_connection.assert_called_once()
