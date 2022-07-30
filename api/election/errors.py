from apiflask import HTTPError


class ElectionDoesNotExist(HTTPError):
    message: str = "An election with the given ID does not exist"
    status_code: int = 404


class OfficeDoesNotExist(HTTPError):
    message: str = "An office with the given ID does not exist"
    status_code: int = 404


class CandidateDoesNotExist(HTTPError):
    message: str = "A candidate with the given ID does not exist"
    status_code: int = 404
