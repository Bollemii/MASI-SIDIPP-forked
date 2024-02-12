from enum import StrEnum


class MessageHeader(StrEnum):
    """Enum class to represent the message header"""

    ACK = "ACK"
    ACCEPT = "ACCEPT"
    ADD_MEMBER = "ADD_MEMBER"
    CREATE_IDEA = "CREATE_IDEA"
    CREATE_OPINION = "CREATE_OPINION"
    DATA = "DATA"
    DATABASE = "DATABASE"
    DECONNECTION = "DECONNECTION"
    INVITATION = "INVITATION"
    PING = "PING"
    PONG = "PONG"
    REJECT = "REJECT"
    REQUEST_PARENT = "REQUEST_PARENT"
