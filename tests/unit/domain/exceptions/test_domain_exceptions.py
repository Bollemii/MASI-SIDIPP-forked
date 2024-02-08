import pytest
from src.domain.exceptions.parent_not_found_error import ParentNotFoundError


class TestDomainExceptions:
    """Test domain exceptions"""

    message = "Error message"

    @pytest.mark.parametrize(
        "exception",
        [
            ParentNotFoundError(message),
        ],
    )
    def test_parent_not_found_creation(self, exception):
        """Test that it is possible to create an exception"""
        assert exception is not None

    @pytest.mark.parametrize(
        "exception",
        [
            ParentNotFoundError(message),
        ],
    )
    def test_parent_not_found_creation_with_message(self, exception):
        """Test that it is possible to create an exception with a message"""
        assert exception.message == self.message

    @pytest.mark.parametrize(
        "exception",
        [
            ParentNotFoundError(message),
        ],
    )
    def test_parent_not_found_creation_to_string(self, exception):
        """Test the to string method of the exception"""
        assert str(exception) == self.message
