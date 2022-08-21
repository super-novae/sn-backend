from sys import exc_info

from .models import Organization
from .schema import OrganizationSchema, OrganizationModifySchema
from .errors import OrganizationNotFound
from api.extensions import db, logger
from api.generic.methods import has_roles
from api.generic.errors import UserDoesNotHaveRequiredRoles
from api.generic.responses import GenericMessage
from apiflask import APIBlueprint, abort
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
    description="An endpoint for the creation of an organization",
    responses=[201, 403, 404],
)
@jwt_required()
def organization_create(data):
    error = False

    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    new_organizatioon = Organization(**data)

    try:
        db.session.add(new_organizatioon)
        db.session.commit()

    except Exception:
        error = True
        logger.warning(exc_info())
        db.session.rollback()
        abort(500)

    finally:
        db.session.close()

    if not error:
        return new_organizatioon


@organization.put("/<id>")
@organization.input(OrganizationModifySchema)
@organization.output(OrganizationSchema)
@organization.doc(
    summary="Organization Modify By Id",
    description="An endpoint for modification of an organization",
    responses=[200, 403, 404],
)
@jwt_required()
def organization_modify_by_id(id, data):
    error = False

    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_id(id)

    if organization:
        for attribute, value in data.items():
            setattr(organization, attribute, value)
        try:
            db.session.commit()

        except Exception:
            error = True
            logger.warning(exc_info())
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

        if not error:
            return organization

    raise OrganizationNotFound


@organization.delete("/<id>")
@organization.output(GenericMessage)
@organization.doc(
    summary="Organization Delete By Id",
    description="An endpoint for the deletion of an organization",
    responses=[200, 403, 404],
)
@jwt_required()
def organization_delete_by_id(id):
    error = False

    user_has_required_roles = has_roles(["super"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization = Organization.find_by_id(id)

    if organization:
        try:
            db.session.delete(organization)
            db.session.commit()

        except Exception:
            error = True
            logger.warning(exc_info())
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

        if not error:
            return {
                "message": f"Organization <{organization.id}> deleted successfully."
            }, 200
    raise OrganizationNotFound
