from enum import StrEnum


class MessageHeader(StrEnum):
    """Enum class to represent the message header"""

    ACK = "ACK"
    ADD_MEMBER = "ADD_MEMBER"
    CREATE_IDEA = "CREATE_IDEA"
    CREATE_OPINION = "CREATE_OPINION"
    DATA = "DATA"
    DATABASE = "DATABASE"
    INVITATION = "INVITATION"
    REJECT = "REJECT"
