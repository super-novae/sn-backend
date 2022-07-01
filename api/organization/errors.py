from apiflask import HTTPError


class OrganizationNotFound(HTTPError):
    status_code: int = 404
    message: str = "Organization with the given ID does not exists"
