from sanic.exceptions import SanicException


class ProhibitedException(SanicException):
    def __init__(self, message=None, status_code=None, *args, **kwargs):
        self.message = message
        self.status_code = status_code
        super().__init__(message=message, status_code=status_code or 403, *args, **kwargs)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'<{self.__class__} code={self.status_code}: {self.message}>'

