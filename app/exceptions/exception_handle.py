from fastapi import status

from app.enums import (
    DATA_NOT_FOUND,
    DUPLICATE_VALUE_ERROR,
    ERROR_OCCURRED,
    INVALID_CREDENTIALS,
)


class ExceptionBase(Exception):

    def __init__(
        self,
        message=ERROR_OCCURRED,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class UniqueViolation(ExceptionBase):

    def __init__(
        self,
        message=DUPLICATE_VALUE_ERROR,
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, status_code)


class NotFound(ExceptionBase):

    def __init__(
        self,
        message=DATA_NOT_FOUND,
        status_code=status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(message, status_code)


class JWTBaseError(ExceptionBase):

    def __init__(
        self,
        message=INVALID_CREDENTIALS,
        status_code=status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)
