from apiflask import HTTPError


class SuperuserWithCredentialsDoesNotExist(HTTPError):
    status_code: int = 404
    message: str = "Superuser with the given credentials does not exist"
