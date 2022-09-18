from apiflask import APIBlueprint
from flask_jwt_extended import create_access_token
from .errors import SuperuserWithCredentialsDoesNotExist
from .models import Superuser
from .schema import SuperuserLoginSchema, SuperUserSchema
from api.extensions import logger

# Initiate Super User module blueprint
superuser = APIBlueprint(
    "superuser", __name__, tag="Superuser", url_prefix="/api/v1/superuser"
)


@superuser.post("/login")
@superuser.input(
    SuperuserLoginSchema,
    example={"username": "tturner", "password": "averycomplexpassword"},
)
@superuser.output(
    SuperUserSchema,
    example={
        "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    },
)
@superuser.doc(
    summary="Superuser Login",
    description="An endpoint for login of the superuser\n\nRoles: *",
    responses=[200, 404],
)
def superuser_login(data):
    superuser: Superuser = Superuser.find_by_username(
        username=data["username"]
    )

    if superuser:
        superuser_password_is_correct = superuser.verify_superuser(
            password=data["password"]
        )
        if superuser_password_is_correct:
            superuser.auth_token = create_access_token(superuser.id)
            return superuser
    logger.warning("Wrong superuser login credentials provided")
    raise SuperuserWithCredentialsDoesNotExist
