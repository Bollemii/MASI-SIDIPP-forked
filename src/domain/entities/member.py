from datetime import datetime


class Member:
    """Member class"""

    def __init__(
        self,
        authentication_key: str,
        ip_address: str,
        port: int,
        creation_date=datetime.now(),
        last_connection_date: datetime | None = None,
    ):
        self.authentication_key = authentication_key
        self.ip_address = ip_address
        self.port = port
        self.creation_date = creation_date
        self.last_connection_date = last_connection_date

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Member):
            return False
        return self.authentication_key == __value.authentication_key

    def to_str(self) -> str:
        """Returns a string representation of the idea."""
        auth_key = self.authentication_key
        creation_date = self.creation_date.isoformat()
        last_connection_date = (
            self.last_connection_date.isoformat()
            if self.last_connection_date is not None
            else "None"
        )
        return f"{auth_key},{self.ip_address},{self.port},{creation_date},{last_connection_date}"

    @classmethod
    def from_str(cls, __value: str) -> "Member":
        """Returns an instance of the Member class from a string."""
        auth_key, ip_address, port, creation_date, last_connection_date = __value.split(
            ",", maxsplit=4
        )
        creation_date = datetime.fromisoformat(creation_date)
        last_connection_date = (
            datetime.fromisoformat(last_connection_date)
            if last_connection_date != "None"
            else None
        )
        return cls(auth_key, ip_address, int(port), creation_date, last_connection_date)
