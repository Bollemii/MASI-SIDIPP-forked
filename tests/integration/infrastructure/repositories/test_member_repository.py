from datetime import datetime
import os
import pytest

from src.domain.entities.member import Member
from src.infrastructure.repositories.member_repository import MemberRepository
from src.application.exceptions.member_already_exists_error import (
    MemberAlreadyExistsError,
)


class TestMemberRepository:
    """Test suite for the MemberRepository class"""

    @pytest.fixture(scope="function", autouse=True, name="member")
    def create_member(self) -> Member:
        """Create a community for the test."""
        member = Member("abc", "127.0.0.1", 1024)
        return member

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_community_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_add_member_to_community(self, temp_folder, member: Member):
        """Validates that it is possible to add a member to a community"""
        community_id = "1234"
        repository = MemberRepository(temp_folder)

        repository.add_member_to_community(community_id, member)

        assert os.path.exists(f"{temp_folder}/{community_id}.sqlite")

    def test_add_member_twice_fails(self, temp_folder, member: Member):
        """Test that adding a community twice fails"""
        repository = MemberRepository(temp_folder)
        repository.add_member_to_community("1234", member)

        with pytest.raises(MemberAlreadyExistsError):
            repository.add_member_to_community("1234", member)

    def test_get_member_from_community_returns_none_when_not_found(self, temp_folder):
        """Validates that None is returned when no member is found"""
        community_id = "1234"
        authentication_key = "abc"
        repository = MemberRepository(temp_folder)

        member = repository.get_member_for_community(community_id, authentication_key)

        assert member is None

    def test_get_member_from_community(self, temp_folder):
        """Validates that it is possible to get a member of a specific community"""
        community_id = "1234"
        authentication_key = "abc"
        member = Member(authentication_key, "127.0.0.1", 1024)
        repository = MemberRepository(temp_folder)
        repository.add_member_to_community(community_id, member)

        member = repository.get_member_for_community(community_id, authentication_key)

        assert member.authentication_key == authentication_key

    @pytest.mark.parametrize(
        "members",
        [
            [Member("abc", "127.0.0.1", 0)],
            [
                Member("abc", "127.0.0.1", 0),
                Member("abc2", "127.0.0.2", 0),
            ],
            [
                Member("abc", "127.0.0.1", 0),
                Member("abc2", "127.0.0.2", 0),
                Member("abc3", "127.0.0.3", 0),
            ],
        ],
    )
    def test_get_members_from_community(self, temp_folder, members):
        """Validates that it is possible to get all members of a specific community"""
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        actual_members = repository.get_members_from_community(community_id)

        assert len(actual_members) == len(members)

    def test_get_members_from_community_returns_empty_list_when_no_members(
        self, temp_folder
    ):
        """Validates that an empty list is returned when no members are found"""
        community_id = "1234"
        repository = MemberRepository(temp_folder)

        members = repository.get_members_from_community(community_id)

        assert len(members) == 0

    def test_get_members_from_community_related(self, temp_folder):
        """Validates that it is possible to get all related members"""
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]

        community_id = "1234"
        repository = MemberRepository(temp_folder)
        repository.add_member_to_community(community_id, members[0], "parent")
        repository.add_member_to_community(community_id, members[1])
        repository.add_member_to_community(community_id, members[2], "child")

        actual_members = repository.get_members_from_community(community_id, True)

        assert len(actual_members) == 2

    def test_get_member_for_community_with_address(self, temp_folder):
        """Validates that it is possible to get a member of a specific community"""
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        ip_address = "127.0.0.1"
        member = repository.get_member_for_community(
            community_id, ip_address=ip_address
        )

        assert member is not None
        assert member.ip_address == ip_address

    def test_get_member_for_community_with_unknown_address(self, temp_folder):
        """Validates that it is possible to get a member of a specific community"""
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        ip_address = "1.1.1.1"
        member = repository.get_member_for_community(
            community_id, ip_address=ip_address
        )

        assert member is None

    def test_get_member_for_community_with_auth_key(self, temp_folder):
        """Validates that it is possible to get a member of a specific community"""
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        auth_key = "abc"
        member = repository.get_member_for_community(
            community_id, member_auth_key=auth_key
        )

        assert member is not None
        assert member.authentication_key == auth_key

    def test_get_member_for_community_with_auth_key_and_address(self, temp_folder):
        """Validates that it is possible to get a member of a specific community"""
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        ip_address = "127.0.0.1"
        auth_key = "abc"
        member = repository.get_member_for_community(community_id, auth_key, ip_address)

        assert member is not None
        assert member.authentication_key == auth_key
        assert member.ip_address == ip_address

    def test_get_member_for_community_with_no_match_auth_key_and_address(
        self, temp_folder
    ):
        """Validates that it is possible to get a member of a specific community"""
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        ip_address = "127.0.0.3"
        auth_key = "abc"
        member = repository.get_member_for_community(community_id, auth_key, ip_address)

        assert member is None

    def test_get_member_for_community_with_no_parameter(self, temp_folder):
        """Get a member with no parameters should raise an error"""
        repository = MemberRepository(temp_folder)

        with pytest.raises(ValueError):
            repository.get_member_for_community("1234")

    def test_clear_members_relationship(self, temp_folder):
        """Validates that it is possible to clear the relationship of all members"""
        members = [
            Member("abc", "127.0.0.1", 0),
            Member("abc2", "127.0.0.2", 0),
            Member("abc3", "127.0.0.3", 0),
        ]
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        repository.add_member_to_community(community_id, members[0], "child")
        repository.add_member_to_community(community_id, members[1], "parent")
        repository.add_member_to_community(community_id, members[2], "None")

        repository.clear_members_relationship(community_id)

    def test_update_member_relationship(self, temp_folder):
        """Validates update the relationship of a member in a specific community"""
        member = Member("abc", "127.0.0.1", 0)
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        repository.add_member_to_community(community_id, member)

        repository.update_member_relationship(
            community_id, member.authentication_key, "child"
        )

    def test_get_older_members(self, temp_folder):
        """Validates that it is possible to get older members"""
        members = [
            Member("abc", "127.0.0.1", 0, datetime(1970, 1, 1)),
            Member("abc2", "127.0.0.2", 0, datetime(1999, 1, 1)),
            Member("abc3", "127.0.0.3", 0, datetime(2023, 1, 1)),
        ]

        community_id = "1234"
        dt = datetime(2000, 1, 1)
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        actual_members = repository.get_older_members_from_community(community_id, dt)

        assert len(actual_members) == 2

    def test_get_older_members_than(self, temp_folder):
        """Validates that it is possible to get older members"""
        members = [
            Member("abc", "127.0.0.1", 0, datetime(1970, 1, 1)),
            Member("abc2", "127.0.0.2", 0, datetime(1999, 1, 1)),
            Member("abc3", "127.0.0.3", 0, datetime(2023, 1, 1)),
        ]

        community_id = "1234"
        dt = datetime(2000, 1, 1)
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        actual_members = repository.get_older_members_from_community(community_id, dt)

        for member in actual_members:
            assert member.creation_date < dt

    def test_get_older_members_ordered(self, temp_folder):
        """Validates that it is possible to get older members"""
        members = [
            Member("abc", "127.0.0.1", 0, datetime(1970, 1, 1)),
            Member("abc2", "127.0.0.2", 0, datetime(1999, 1, 1)),
            Member("abc3", "127.0.0.3", 0, datetime(2023, 1, 1)),
        ]

        community_id = "1234"
        dt = datetime(2000, 1, 1)
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        actual_members = repository.get_older_members_from_community(community_id, dt)

        for i in range(1, len(actual_members)):
            assert (
                actual_members[i].creation_date >= actual_members[i - 1].creation_date
            )
