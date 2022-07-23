from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from api.extensions import db
from .errors import *
from .models import Administrator
from .schema import *
from api.generic.methods import has_roles
from api.generic.errors import *

# Initiate module blueprint
administrator = APIBlueprint(
    "administrator",
    __name__,
    tag="Administrator",
    url_prefix="/api/v1/administrators",
)


@administrator.post("/signup")
@administrator.input(AdministratorSchema)
@administrator.output(AdministratorSchema)
@administrator.doc(
    summary="Administrator Sign Up",
    description="An endpoint for the creation of administrators",
    responses=[200, 409],
)
@jwt_required()
def administrator_sign_up(data):
    # Perform security checks
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    # Checking if admin with the same email exists
    admin_email_exists = Administrator.find_by_email(data["email"])
    if admin_email_exists:
        raise AdministratorWithEmailExists

    # Check if admin with the same username exists
    admin_username_exists = Administrator.find_by_username(data["username"])
    if admin_username_exists:
        raise AdministratorWithUsernameExists

    # Create admin instance
    admin = Administrator(**data)
    admin.password = data["password"]

    # Commit to database
    db.session.add(admin)
    db.session.commit()

    return admin


@administrator.post("/login")
@administrator.input(AdministratorLoginInputSchema)
@administrator.output(AdministratorLoginOutputSchema)
@administrator.doc(
    summary="Administrator Login",
    description="An endpoint for the login of administrators",
)
def administrator_login(data):
    admin = Administrator.find_by_email(data["email"])

    if admin:
        admin_password_is_correct = admin.verify_password(data["password"])
        if admin_password_is_correct:
            admin.auth_token = create_access_token(admin.id)
            return admin
    raise AdministratorWithCredentialsDoesNotExist


@administrator.get("/")
@administrator.output(AdministratorsSchema)
@administrator.doc(
    summary="Administrator Get All",
    description="An endpoint to get all administrators",
)
@jwt_required()
def administrator_get_all():
    # Perform security checks
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    admins = Administrator.get_all()

    return {"administrators": admins}


@administrator.get("/<admin_id>")
@administrator.output(AdministratorSchema)
@administrator.doc(
    summary="Administrator Get By Id",
    description="An endpoint to an administrator by ID",
)
@jwt_required()
def administrator_get_by_id(admin_id):
    # Perform security checks
    user_has_required_roles = has_roles(["super", "admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    admin = Administrator.find_by_id(admin_id)
    if admin:
        return admin

    raise AdministratorWithCredentialsDoesNotExist
