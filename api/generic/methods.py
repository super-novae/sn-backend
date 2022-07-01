from api.administrator.models import Administrator
from api.superuser.models import Superuser

# from api.voter.models import Voter
from .errors import *


def has_roles(role_list, public_id):
    # TODO: Possible optimization
    roles = {"super": Superuser, "admin": Administrator}
    # roles = {"super": Superuser, "admin": Administrator, "voter": Voter}

    current_user_roles = []
    for role in role_list:
        current_user_roles.append(roles[role].find_by_public_id(public_id))
    return any(current_user_roles)
