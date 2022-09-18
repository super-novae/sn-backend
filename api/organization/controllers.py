from .models import Organization
from .schema import (
    OrganizationSchema,
    OrganizationModifySchema,
    OrganizationsSchema,
)
from .errors import OrganizationNotFound
from api.administrator.schema import AdministratorSchema
from api.administrator.models import Administrator
from api.generic.db import save, modify, delete
from api.generic.methods import has_roles
from api.generic.errors import UserDoesNotHaveRequiredRoles
from api.generic.responses import GenericMessage
from apiflask import APIBlueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

organization = APIBlueprint(
    "organization",
    __name__,
    tag="Organization",
    url_prefix="/api/v1/organization",
)


@organization.post("/")
@organization.input(OrganizationSchema)
@organization.output(OrganizationSchema, status_code=201)
@organization.doc(
    summary="Organization Create",
    description="An endpoint for the creation of an organization\n\nRoles: SUPERUSER",
    responses=[201, 403, 404],
)
@jwt_required()
def organization_create(data):

    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    new_organization = Organization(**data)

    new_organization, error = save(new_organization)

    if not error:
        return new_organization


@organization.put("/<id>")
@organization.input(OrganizationModifySchema)
@organization.output(OrganizationSchema)
@organization.doc(
    summary="Organization Modify By Id",
    description="An endpoint for modification of an organization\n\nRoles: SUPERUSER",
    responses=[200, 403, 404],
)
@jwt_required()
def organization_modify_by_id(id, data):
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_id(id)

    if organization:
        for attribute, value in data.items():
            setattr(organization, attribute, value)

        organization, error = modify(organization)

        if not error:
            return organization

    raise OrganizationNotFound


@organization.delete("/<id>")
@organization.output(GenericMessage)
@organization.doc(
    summary="Organization Delete By Id",
    description="An endpoint for the deletion of an organization\n\nRoles: SUPERUSER",
    responses=[200, 403, 404],
)
@jwt_required()
def organization_delete_by_id(id):
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_id(id)

    if organization:
        organization, error = delete(organization)

        if not error:
            return {
                "message": f"Organization <{organization.id}> deleted successfully."
            }, 200
    raise OrganizationNotFound


@organization.get("/<id>")
@organization.output(OrganizationSchema)
@organization.doc(
    summary="Organization Get By Id",
    description="An endpoint for the deletion of an organization\n\nRoles: SUPERUSER, ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def organization_get_by_id(id):
    user_has_required_roles = has_roles(["super", "admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_id(id)

    if not organization:
        raise OrganizationNotFound

    return organization, 200


@organization.get("/<id>/administrator")
@organization.output(AdministratorSchema)
@organization.doc(
    summary="Organization Get Administrator By Id",
    description="An endpoint to get the administrator of an organization\n\nRoles: SUPERUSER",
    responses=[200, 403, 404],
)
@jwt_required()
def organization_get_administrator(id):
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_id(id)
    if not organization:
        raise OrganizationNotFound

    administrator = Administrator.find_by_id(organization.administrator_id)

    return administrator, 200


@organization.get("/")
@organization.output(OrganizationsSchema)
@organization.doc(
    summary="Organization Get All",
    description="An endpoint to get all registered organizations\n\nRoles: SUPERUSER",
    responses=[200, 403],
)
@jwt_required()
def organization_get_all():
    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organizations = Organization.find_all()

    return {"organizations": organizations}, 200
