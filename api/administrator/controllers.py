from apiflask import APIBlueprint
from .models import Administrator
from .schema import AdministratorSchema, AdministratorsSchema, AdministratorLoginSchema
from .errors import AdministratorNotFound

# Initiate module blueprint
administrator = APIBlueprint(
    "administrator",
    __name__,
    tag="Administrator",
    url_prefix="/api/v1/elections/<election_id>/administrators",
)


@administrator.post("/signup")
@administrator.input(AdministratorSchema)
@administrator.output(AdministratorSchema)
@administrator.doc(
    summary="Administrator Sign Up",
    description="An endpoint for the creation of administrators",
)
def administrator_sign_up(election_id, data):
    pass


@administrator.post("/login")
@administrator.input(AdministratorLoginSchema)
@administrator.output(AdministratorSchema)
@administrator.doc(
    summary="Administrator Login",
    description="An endpoint for the login of administrators",
)
def administrator_login(election_id, data):
    pass


@administrator.get("/")
@administrator.output(AdministratorsSchema)
@administrator.doc(
    summary="Administrator Get All",
    description="An endpoint to get all administrators",
)
def administrator_get_all(election_id):
    pass


@administrator.get("/<admin_id>")
@administrator.output(AdministratorSchema)
@administrator.doc(
    summary="Administrator Get By Id",
    description="An endpoint to an administrator by ID",
)
def administrator_get_by_id(election_id, id):
    raise AdministratorNotFound
