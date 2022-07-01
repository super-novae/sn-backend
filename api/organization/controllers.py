from .models import Organization
from .schema import OrganizationSchema
from .errors import OrganizationNotFound
from api.extensions import db
from api.generic.methods import has_roles
from api.generic.errors import UserDoesNotHaveRequiredRoles
from apiflask import APIBlueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

organization = APIBlueprint(
    "organization", __name__, tag="Organization", url_prefix="/api/v1/organization"
)


@organization.post("/")
@organization.input(OrganizationSchema)
@organization.output(OrganizationSchema)
@jwt_required()
def organization_create(data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    new_organizatioon = Organization(**data)

    db.session.add(new_organizatioon)
    db.session.commit()

    return new_organizatioon


@organization.put("/<id>")
@organization.input(OrganizationSchema)
@organization.output(OrganizationSchema)
@jwt_required()
def organization_modify_by_id(id, data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_public_id(id)

    if organization:
        for attribute, value in data.items():
            setattr(organization, attribute, value)

        db.session.commit()

        return organization

    raise OrganizationNotFound


@organization.delete("/<id>")
@jwt_required()
def organization_delete_by_id(id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_public_id(id)

    if organization:
        db.session.delete(organization)
        db.session.commit()

        return {
            "message": f"Organization <{organization.public_id}> deleted successfully.",
            "status_code": 200,
        }
    raise OrganizationNotFound
