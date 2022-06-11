from apiflask import HTTPError


class AdministratorNotFound(HTTPError):
    status_code: int = 404
    message: str = "Administrator account not found"
