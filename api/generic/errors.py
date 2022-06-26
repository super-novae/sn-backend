from apiflask import HTTPError


class UserDoesNotHaveRequiredRoles(HTTPError):
    message: str = "User does not have the required permissions to perform action"
    status_code: int = 403
