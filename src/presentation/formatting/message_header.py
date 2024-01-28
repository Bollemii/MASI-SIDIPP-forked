from enum import StrEnum


class MessageHeader(StrEnum):
    """Enum class to represent the message header"""

    ACK = "ACK"
    CREATE_IDEA = "CREATE_IDEA"
    CREATE_OPINION = "CREATE_OPINION"
    DATA = "DATA"
    DATABASE = "DATABASE"
    INFORMATIONS = "INFORMATIONS"
    INVITATION = "INVITATION"
    REJECT = "REJECT"
