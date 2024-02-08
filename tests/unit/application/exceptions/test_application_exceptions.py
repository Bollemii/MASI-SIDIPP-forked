import pytest
from src.application.exceptions.authentification_failed_error import (
    AuthentificationFailedError,
)
from src.application.exceptions.community_already_exists_error import (
    CommunityAlreadyExistsError,
)
from src.application.exceptions.idea_already_exists_error import (
    OpinionAlreadyExistsError,
)
from src.application.exceptions.member_already_exists_error import (
    MemberAlreadyExistsError,
)
from src.application.exceptions.message_error import MessageError
from src.application.exceptions.opinion_already_exists_error import (
    IdeaAlreadyExistsError,
)
from src.application.exceptions.socket_error import SocketError


class TestApplicationExceptions:
    """Test application exceptions."""

    message = "Error message"

    @pytest.mark.parametrize(
        "exception",
        [
            AuthentificationFailedError(message),
            CommunityAlreadyExistsError(message),
            IdeaAlreadyExistsError(message),
            MemberAlreadyExistsError(message),
            MessageError(message),
            OpinionAlreadyExistsError(message),
            SocketError(message),
        ],
    )
    def test_authentication_failed(self, exception):
        """Test that it is possible to create an exception"""
        assert exception is not None

    @pytest.mark.parametrize(
        "exception",
        [
            AuthentificationFailedError(message),
            CommunityAlreadyExistsError(message),
            IdeaAlreadyExistsError(message),
            MemberAlreadyExistsError(message),
            MessageError(message),
            OpinionAlreadyExistsError(message),
            SocketError(message),
        ],
    )
    def test_authentication_failed_message(self, exception):
        """Test that it is possible to create an exception with a message"""
        assert exception.inner_error == self.message

    @pytest.mark.parametrize(
        "exception",
        [
            AuthentificationFailedError(message),
            CommunityAlreadyExistsError(message),
            IdeaAlreadyExistsError(message),
            MemberAlreadyExistsError(message),
            MessageError(message),
            OpinionAlreadyExistsError(message),
            SocketError(message),
        ],
    )
    def test_authentication_failed_to_string(self, exception):
        """Test the to string method of the exception"""
        assert self.message in str(exception)
