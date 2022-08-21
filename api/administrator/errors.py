from apiflask import HTTPError


class AdministratorWithEmailExists(HTTPError):
    status_code: int = 409
    message: str = "Administrator with this email already exists."


class AdministratorWithUsernameExists(HTTPError):
    status_code: int = 409
    message: str = "Administrator with this username already exists."


class AdministratorWithCredentialsDoesNotExist(HTTPError):
    status_code: int = 404
    message: str = "Administrator with the given credentials does not exist."


class AdministratorWithIdDoesNotExist(HTTPError):
    status_code: int = 404
    message: str = "Administrator with the given Id does not exist"


class AdministratorTokenExpired(HTTPError):
    status_code: int = 401
    message: str = "Administrator token expired. Please login again."


class AdministratorTokenInvalid(HTTPError):
    status_code: int = 401
    message: str = "Administrator token is invalid. Please login again."
