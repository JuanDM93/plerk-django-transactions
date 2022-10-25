class BaseCustomError(Exception):

    def __init__(
        self,
        message: str = "Unknown error",
        error_code: int = 5000,
        status_code: int = 500,
    ):
        """
        Exception to raise when an error has occurred and it has error_code.
        """
        self.error_code = error_code
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message


class BasicError(BaseCustomError):

    def __init__(self, message: str, status: int):
        super().__init__(message=message, status=status)


class CustomError(BaseCustomError):
    pass
