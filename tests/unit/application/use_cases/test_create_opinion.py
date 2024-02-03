from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.create_opinion import CreateOpinion
from src.domain.entities.idea import Idea
from src.domain.entities.member import Member
from src.domain.entities.opinion import Opinion


class TestCreateOpinion:
    """Test suite around creating an opinion."""

    @pytest.fixture(scope="function", autouse=True, name="author")
    def create_member(self):
        """Create a member instance."""
        return Member("auth_key1", "127.0.0.1", 1664)

    @pytest.fixture(scope="function", autouse=True, name="create_opinion_usecase")
    @mock.patch(
        "src.application.interfaces.iarchitecture_manager", name="architecture_manager"
    )
    @mock.patch(
        "src.application.interfaces.icommunity_manager", name="community_manager"
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
        "src.application.interfaces.iopinion_repository", name="opinion_repo_mock"
    )
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
        opinion_repo_mock: MagicMock,
        symetric_encryption_service_mock: MagicMock,
        datetime_service_mock: MagicMock,
        community_manager: MagicMock,
        architecture_manager: MagicMock,
    ):
        """Create a usecase instance."""
        symetric_encryption_service_mock.encrypt.return_value = (
            "nonce",
            "tag",
            "cipher",
        )

        return CreateOpinion(
            machine_service_mock,
            id_generator_service_mock,
            idea_repo_mock,
            opinion_repo_mock,
            symetric_encryption_service_mock,
            datetime_service_mock,
            community_manager,
            architecture_manager,
        )

    @pytest.fixture(scope="function", autouse=True, name="idea")
    def create_idea(self):
        """Create an idea instance."""
        return Idea("1", "content", Member("abc", "127.0.0.1", 1664))

    def test_create_opinion_calls_repository_for_idea(
        self,
        create_opinion_usecase: CreateOpinion,
        idea: Idea,
    ):
        """Creating an opinion should be possible given the proper arguments."""
        create_opinion_usecase.idea_repository.get_idea_from_community.return_value = (
            idea
        )

        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.idea_repository.get_idea_from_community.assert_called_once()
        create_opinion_usecase.opinion_repository.get_opinion_from_community.assert_not_called()
        create_opinion_usecase.opinion_repository.add_opinion_to_community.assert_called_once()

    def test_create_opinion_calls_repository_for_opinion(
        self,
        create_opinion_usecase: CreateOpinion,
        idea: Idea,
    ):
        """Creating an opinion should be possible given the proper arguments."""
        create_opinion_usecase.idea_repository.get_idea_from_community.return_value = (
            None
        )
        create_opinion_usecase.opinion_repository.get_opinion_from_community.return_value = Opinion(
            "1", "content", Member("abc", "127.0.0.1", 1664), datetime.now(), idea
        )
        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.idea_repository.get_idea_from_community.assert_called_once()
        create_opinion_usecase.opinion_repository.get_opinion_from_community.assert_called_once()
        create_opinion_usecase.opinion_repository.add_opinion_to_community.assert_called_once()

    def test_create_opinion_encrypts_data(
        self,
        create_opinion_usecase: CreateOpinion,
    ):
        """Creating an opinion should call the symetric encryption method"""
        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.symetric_encryption_service.encrypt.assert_called()

    def test_create_opinion_reads_symetric_key_file(
        self,
        create_opinion_usecase: CreateOpinion,
    ):
        """Creating an opinion should call the symetric encryption method"""
        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.community_manager.get_community_symetric_key.assert_called()

    def test_success_output(self, create_opinion_usecase: CreateOpinion):
        """Creating an opinion should return a success output."""
        output = create_opinion_usecase.execute("1", "1", "content")

        assert output == "Success!"

    def test_error_output(self, create_opinion_usecase: CreateOpinion):
        """Creating an opinion should return an error output."""
        create_opinion_usecase.idea_repository.get_idea_from_community.side_effect = (
            Exception()
        )

        output = create_opinion_usecase.execute("1", "1", "content")

        assert output != "Success!"

    def test_create_opinion_should_call_datetime_service(
        self, create_opinion_usecase: CreateOpinion
    ):
        """Creating an opinion should call the datetime service."""
        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.datetime_service.get_datetime.assert_called_once()

    def test_create_opinion_share_message_to_community(
        self, create_opinion_usecase: CreateOpinion
    ):
        """Creating an opinion should call the architecture manager to share the message."""
        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.architecture_manager.share.assert_called_once()

    def test_create_opinion_with_invalid_content(
        self, create_opinion_usecase: CreateOpinion
    ):
        """Creating an opinion should return an error message if the content is invalid."""
        result = create_opinion_usecase.execute("1", "1", "c")

        assert result != "Success!"
