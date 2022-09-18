from apiflask import APIBlueprint
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

from ..generic.responses import GenericMessage
from ..generic.db import delete, save, modify
from ..generic.password import generate_password
from ..generic.mail import send_password_to_admin
from .errors import (
    AdministratorWithIdDoesNotExist,
    AdministratorWithCredentialsDoesNotExist,
    AdministratorWithEmailExists,
    AdministratorWithUsernameExists,
)
from .models import Administrator
from .schema import (
    AdministratorSchema,
    AdministratorsSchema,
    AdministratorLoginInputSchema,
    AdministratorLoginOutputSchema,
    AdministratorModifySchema,
)
from api.generic.methods import has_roles
from api.generic.errors import UserDoesNotHaveRequiredRoles

# Initiate module blueprint
administrator = APIBlueprint(
    "administrator",
    __name__,
    tag="Administrator",
    url_prefix="/api/v1/administrators",
)


@administrator.post("/signup")
@administrator.input(AdministratorSchema)
@administrator.output(AdministratorSchema, status_code=201)
@administrator.doc(
    summary="Administrator Sign Up",
    description="An endpoint for the creation of administrators \n\nRoles: SUPERUSER",
    responses=[201, 403, 409],
)
@jwt_required()
def administrator_sign_up(data):
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
    password = generate_password()

    admin.password = password

    send_password_to_admin(admin.email, admin.name, password)

    admin, error = save(admin)

    if not error:
        return admin, 201


@administrator.put("/<admin_id>")
@administrator.input(AdministratorModifySchema)
@administrator.output(GenericMessage)
@administrator.doc(
    summary="Administrator Modify By Id",
    description="An endpoint to modify an administrator by id \n\nRoles: SUPERUSER",
    responses=[200, 403, 404],
)
@jwt_required()
def administrator_modify(admin_id, data):
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    admin = Administrator.find_by_id(admin_id)
    if not admin:
        raise AdministratorWithIdDoesNotExist

    # Checking if admin with the same email exists
    if data.get("email", None):
        admin_email_exists = Administrator.find_by_email(data["email"])
        if admin_email_exists:
            raise AdministratorWithEmailExists

    # Check if admin with the same username exists
    if data.get("username", None):
        admin_username_exists = Administrator.find_by_username(
            data["username"]
        )
        if admin_username_exists:
            raise AdministratorWithUsernameExists

    for attribute, value in data.items():
        setattr(admin, attribute, value)
    admin, error = modify(admin)

    if not error:
        return {"message": "Administrator modified successfully"}, 200


@administrator.delete("/<admin_id>")
@administrator.output(GenericMessage)
@administrator.doc(
    summary="Administrator Delete",
    description="An endpoint for the deletion of an administrator \n\nRoles: SUPERUSER",
    responses=[200, 403, 404],
)
@jwt_required()
def administrator_delete(admin_id):
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    admin = Administrator.find_by_id(admin_id)
    if not admin:
        raise AdministratorWithIdDoesNotExist

    admin, error = delete(admin)

    if not error:
        return {"message": "Administrator deleted successfully"}, 200


@administrator.post("/login")
@administrator.input(AdministratorLoginInputSchema)
@administrator.output(AdministratorLoginOutputSchema)
@administrator.doc(
    summary="Administrator Login",
    description="An endpoint for the login of administrators\n\nRoles: *",
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
    description="An endpoint to get all administrators \n\nRoles: SUPERUSER",
)
@jwt_required()
def administrator_get_all():
    # Perform security checks
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    admins = Administrator.get_all()

    return {"administrators": admins}, 200


@administrator.get("/<admin_id>")
@administrator.output(AdministratorSchema)
@administrator.doc(
    summary="Administrator Get By Id",
    description="An endpoint to an administrator by ID\n\nRoles: SUPERUSER",
)
@jwt_required()
def administrator_get_by_id(admin_id):
    # Perform security checks
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    admin = Administrator.find_by_id(admin_id)
    if admin:
        return admin

    raise AdministratorWithCredentialsDoesNotExist
