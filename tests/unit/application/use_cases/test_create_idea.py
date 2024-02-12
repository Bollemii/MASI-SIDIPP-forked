from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.create_idea import CreateIdea


class TestCreateIdea:
    """Test suite around creating an idea."""

    @pytest.fixture(scope="function", autouse=True, name="create_idea_usecase")
    @mock.patch(
        "src.application.interfaces.iarchitecture_manager", name="architecture_manager"
    )
    @mock.patch(
        "src.application.interfaces.icommunity_service", name="community_service"
    )
    @mock.patch(
        "src.application.interfaces.idatetime_service", name="datetime_service_mock"
    )
    @mock.patch(
        "src.application.interfaces.isymetric_encryption_service",
        name="symetric_encryption_service_mock",
    )
    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repo_mock")
    @mock.patch(
        "src.application.interfaces.iid_generator_service",
        name="id_generator_service_mock",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service", name="machine_service_mock"
    )
    def create_usecase(
        self,
        machine_service_mock: MagicMock,
        id_generator_service_mock: MagicMock,
        idea_repo_mock: MagicMock,
        symetric_encryption_service_mock: MagicMock,
        datetime_service_mock: MagicMock,
        community_service: MagicMock,
        architecture_manager: MagicMock,
    ):
        """Create a usecase instance."""
        symetric_encryption_service_mock.encrypt.return_value = (
            "nonce",
            "tag",
            "cipher",
        )

        return CreateIdea(
            machine_service_mock,
            id_generator_service_mock,
            idea_repo_mock,
            symetric_encryption_service_mock,
            datetime_service_mock,
            community_service,
            architecture_manager,
        )

    def test_create_idea_calls_repository(
        self,
        create_idea_usecase: CreateIdea,
    ):
        """Creating an idea should be possible given the proper arguments."""
        create_idea_usecase.execute("1", "content")

        create_idea_usecase.idea_repository.add_idea_to_community.assert_called_once()

    def test_create_idea_reads_symetric_key_file(self, create_idea_usecase: CreateIdea):
        """Creating an idea should call the community manager to get the symetric key."""
        content = "content"
        create_idea_usecase.id_generator_service.generate.return_value = "123"

        create_idea_usecase.execute("1", content)

        create_idea_usecase.community_service.get_community_symetric_key.assert_called()

    def test_create_idea_encrypts_data(
        self,
        create_idea_usecase: CreateIdea,
    ):
        """Creating an idea should call the symetric encryption service to encrypt the data."""
        create_idea_usecase.id_generator_service.generate.return_value = "123"

        create_idea_usecase.execute("1", "content")

        create_idea_usecase.symetric_encryption_service.encrypt.assert_called()

    def test_success_output(
        self,
        create_idea_usecase: CreateIdea,
    ):
        """Creating an idea should return a success message."""
        output = create_idea_usecase.execute("1", "content")

        assert output == "Success!"

    def test_error_output(
        self,
        create_idea_usecase: CreateIdea,
    ):
        """Creating an idea should return an error message if something goes wrong"""
        create_idea_usecase.id_generator_service.generate.side_effect = Exception()

        output = create_idea_usecase.execute("1", "content")

        assert output != "Success!"

    def test_create_idea_should_call_datetime_service(
        self, create_idea_usecase: CreateIdea
    ):
        """Creating an idea should call the datetime service to get the current datetime."""
        create_idea_usecase.execute("1", "content")

        create_idea_usecase.datetime_service.get_datetime.assert_called_once()

    def test_create_idea_share_message_to_community(
        self, create_idea_usecase: CreateIdea
    ):
        """Creating an idea should call the architecture manager to share the message to the community."""
        create_idea_usecase.execute("1", "content")

        create_idea_usecase.architecture_manager.share_information.assert_called_once()

    def test_create_idea_with_invalid_content(self, create_idea_usecase: CreateIdea):
        """Creating an idea with invalid content should return an error message."""
        result = create_idea_usecase.execute("1", "c")

        assert result != "Success!"
