from datetime import datetime

import pytest

from src.domain.entities.idea import Idea
from src.domain.entities.member import Member


class TestIdea:
    """Test Idea class"""

    @pytest.fixture(scope="function", autouse=True, name="author")
    def fixture_author(self) -> Member:
        """Fixture to create a member"""
        return Member("abc", "127.0.0.1", 1024)

    def test_init(self, author):
        """Validates that an idea can be created"""
        idea = Idea("1", "Text", author, datetime.now())

        assert idea is not None

    def test_id_attribute(self, author: Member):
        """Validates that an idea created with a specified ID has that ID"""
        id_idea = "1"
        idea = Idea(id_idea, "Text", author, datetime.now())

        assert idea.identifier == id_idea

    def test_text_attribute(self, author: Member):
        """Validates that an idea created with a specified text has that text"""
        text_idea = "Text"
        idea = Idea("1", text_idea, author, datetime.now())

        assert idea.content == text_idea

    def test_author_attribute(self, author: Member):
        """Validates that an idea created with a specified author has that author"""
        idea = Idea("1", "Text", author, datetime.now())

        assert idea.author == author

    def test_creation_date_attribute(self, author: Member):
        """Validates that an idea created with a specified creation date has that
        creation date"""
        creation_date_idea = datetime.now()
        idea = Idea("1", "Text", author, creation_date_idea)

        assert idea.creation_date == creation_date_idea

    def test_ideas_equality(self, author: Member):
        """Validates that two ideas with the same ID are equal"""
        idea = Idea("1", "Text", author, datetime.now())
        idea_copy = Idea("1", "Text", author, datetime.now())

        assert idea == idea_copy

    def test_idea_inequality(self, author: Member):
        """Validates that two ideas with different IDs are not equal"""
        idea = Idea("1", "Text", author, datetime.now())
        second_idea = Idea("2", "Text", author, datetime.now())

        assert idea != second_idea

    def test_idea_inequality_with_other_type(self, author: Member):
        """Validates that an idea is not equal to an object of another type"""
        idea = Idea("1", "Text", author, datetime.now())
        other_type = "Text"

        assert idea != other_type

    def test_idea_to_str(self, author: Member):
        """Validates that an idea can be converted to a string"""
        idea = Idea("1", "Text", author, datetime.now())

        assert isinstance(idea.to_str(), str)

    def test_idea_from_str(self, author: Member):
        """Validates that an idea can be created from a string"""
        idea = Idea("1", "Text", author, datetime.now())
        idea_str = idea.to_str()

        assert Idea.from_str(idea_str) == idea
