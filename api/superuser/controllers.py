from apiflask import APIBlueprint
from flask_jwt_extended import create_access_token
from .errors import *
from .models import Superuser
from .schema import *

# Initiate Super User module blueprint
superuser = APIBlueprint(
    "superuser", __name__, tag="Superuser", url_prefix="/api/v1/superuser"
)


@superuser.post("/login")
@superuser.input(SuperuserLoginSchema)
@superuser.output(SuperUserSchema)
@superuser.doc(
    summary="Superuser Login", description="An endpoint for login of the superuser"
)
def superuser_login(data):
    superuser: Superuser = Superuser.find_by_username(username=data["username"])

    if superuser:
        superuser_password_is_correct = superuser.verify_superuser(
            password=data["password"]
        )
        if superuser_password_is_correct:
            superuser.auth_token = create_access_token(superuser.public_id)
            return superuser
    raise SuperuserWithCredentialsDoesNotExist
