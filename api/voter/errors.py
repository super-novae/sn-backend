from apiflask import HTTPError


class VoterDoesNotExist(HTTPError):
    message: str = "A voter with the given Id does not exist"
    status_code: int = 404


class VoterAlreadyExists(HTTPError):
    message: str = "A voter with the given credentials already exists"
    status_code: int = 409


class VoterWrongCredentials(HTTPError):
    message: str = "A voter with the given credentials does not exist"
    status_code: int = 400


class VoterOrganizationIdNotProvided(HTTPError):
    message: str = "No organization provided in the url"
    status_code: int = 400


class VoterHasAlreadyVoted(HTTPError):
    message: str = "Voter has already voted for a candidate in this office"
    status_code: int = 400
