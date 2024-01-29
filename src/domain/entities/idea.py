from datetime import datetime

from src.domain.common.message import Message
from src.domain.entities.member import Member


class Idea(Message):
    """Idea class"""

    # This class is a subclass of Message, so it inherits all the attributes and methods of Message.
    # The __init__ method of this class is overriding the __init__ method of Message.

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Idea):
            return False
        return self.identifier == __value.identifier

    def to_str(self) -> str:
        """Returns a string representation of the idea."""
        author_id = self.author.authentication_key
        date = self.creation_date.isoformat()
        return f"{self.identifier},{self.content},{author_id},{date}"

    @classmethod
    def from_str(cls, __value: str):
        """Returns an instance of the class from a string representation."""
        identifier, content, author_id, creation_date = __value.split(",", maxsplit=3)
        author = Member(author_id, None, None)
        creation_date = datetime.fromisoformat(creation_date)
        return cls(identifier, content, author, creation_date)
