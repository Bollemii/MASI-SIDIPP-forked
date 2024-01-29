from datetime import datetime

from src.domain.common.message import Message
from src.domain.entities.member import Member
from src.domain.entities.idea import Idea  # pylint: disable=unused-import


class Opinion(Message):
    """Opinion class"""

    def __init__(
        self,
        identifier: str,
        content: str,
        author: Member,
        creation_date: datetime,
        parent: "Opinion | Idea",
    ):
        super().__init__(identifier, content, author, creation_date)
        self.parent = parent

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Opinion):
            return False
        return self.identifier == __value.identifier

    def to_str(self) -> str:
        """Returns a string representation of the idea."""
        author_id = self.author.authentication_key
        date = self.creation_date.isoformat()
        parent_id = self.parent.identifier
        return f"{self.identifier},{self.content},{author_id},{date},{parent_id}"

    @classmethod
    def from_str(cls, __value: str) -> "Opinion":
        """Creates an opinion from a string."""
        identifier, content, author_id, creation_date, parent_id = __value.split(
            ",", maxsplit=4
        )
        author = Member(author_id, None, None)
        creation_date = datetime.fromisoformat(creation_date)
        parent = Message(parent_id, None, None, None)
        return cls(identifier, content, author, creation_date, parent)
