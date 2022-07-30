from sanic.exceptions import SanicException


class NotAuthorized(SanicException):
    status_code = 401
    message = "You are not authorized"
