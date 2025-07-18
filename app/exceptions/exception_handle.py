class ExceptionBase(Exception):

    def __init__(self, message="An error occurred"):
        super().__init__(message)
        self.message = message


class UniqueViolation(ExceptionBase):

    def __init__(
        self,
        message="This field must be unique. A duplicate value was found",
    ):
        super().__init__(message)


class NotFound(ExceptionBase):

    def __init__(
        self,
        message="Data not found",
    ):
        super().__init__(message)


class JWTBaseError(ExceptionBase):

    def __init__(
        self,
        message="Invalid credentials",
    ):
        super().__init__(message)
