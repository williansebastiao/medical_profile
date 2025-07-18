from enum import StrEnum


class StatusEnum(StrEnum):
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    PENDING = "PENDING"
    IGNORED = "IGNORED"


class EmailType(StrEnum):
    WELCOME = "WELCOME"
    RESET_PASSWORD = "RESET_PASSWORD"
