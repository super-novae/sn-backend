from api.administrator.models import Administrator
from api.superuser.models import Superuser
from api.voter.models import Voter

# from api.voter.models import Voter
from .errors import *

security_headers = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "Content-Security-Policy": "default-src 'self'",
}


def has_roles(role_list, id):
    roles = {"super": Superuser, "admin": Administrator, "voter": Voter}

    current_user_roles = []
    for role in role_list:
        current_user_roles.append(roles[role].find_by_id(id))
    return any(current_user_roles)
