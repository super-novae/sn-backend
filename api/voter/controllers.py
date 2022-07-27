from .errors import (
    VoterDoesNotExist,
    VoterAlreadyExists,
    VoterOrganizationIdNotProvided,
)
from .models import Voter
from .schema import VoterSchema, VotersSchema, VoterGetAllInputSchema
from apiflask import APIBlueprint
from api.extensions import db
from api.generic.errors import UserDoesNotHaveRequiredRoles
from api.generic.methods import has_roles
from api.organization.errors import OrganizationNotFound
from api.organization.models import Organization
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

voters = APIBlueprint("voter", __name__, tag="Voter", url_prefix="/api/v1/voters")

############################################
##                 VOTER                  ##
############################################
@voters.post("/signup")
@voters.input(VoterSchema)
@voters.output(VoterSchema)
@voters.doc(
    summary="Voter Signup",
    description="An endpoint for voter signup",
    responses=[201, 403],
)
@jwt_required()
def voter_signup(data):
    # TODO: Ask who is supposed to have access to this route
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    voter_email_exists = Voter.find_by_email(data["email"])
    voter_username_exists = Voter.find_by_username(data["username"])

    if voter_email_exists or voter_username_exists:
        return VoterAlreadyExists

    voter = Voter(**data)

    db.session.add()
    db.session.commit()

    return voter, 201


@voters.post("/signup-bulk")
@voters.doc()
def voter_bulk_signup():
    # TODO: Implement later
    pass


@voters.post("/login")
@voters.input(VoterSchema)
@voters.output(VoterSchema)
@voters.doc(
    summary="Voter Login",
    description="An endpoint for voter login",
    responses=[200, 403, 404],
)
def voter_login(data):
    voter: Voter = Voter.find_by_email(data["email"])

    if voter:
        voter_password_is_correct = voter.verify_password(data["password"])
        if voter_password_is_correct:
            voter.auth_token = create_access_token(voter.id)
            return voter, 200
    raise VoterDoesNotExist


@voters.get("/<voter_id>")
@voters.output(VoterSchema)
@voters.doc(
    summary="Voter Get By Id",
    description="An endpoint to get a voter by ID",
    responses=[200, 403, 404],
)
@jwt_required()
def voter_get_by_id(voter_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    voter = Voter.find_by_id(id)
    if voter:
        return voter, 200

    raise VoterDoesNotExist


@voters.get("/")
@voters.input(
    VoterGetAllInputSchema,
    location="query",
    examples=["/?organization_id=org-1234123412341234123412341234"],
)  # TODO: Look at other options provided by input
@voters.output(VotersSchema)
@voters.doc(
    summary="Voter Get All",
    description="An endpoint to get all voters in organization",
    responses=[200, 400, 403],
)
def voter_get_all():
    # Perform security checks
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization_id = request.args.get("organization_id", None)

    if not organization_id:
        organization = Organization.find_by_id(organization_id)
        if organization:
            voters = Voter.find_all_organization_id(organization.id)

            return {"voters": voters}, 200
        raise OrganizationNotFound
    raise VoterOrganizationIdNotProvided


@voters.get("/<id>/elections")
@voters.doc(
    summary="Voter Elections",
    description="An endpoint to get all mini elections for voter",
)
def voter_get_elections(id, data):
    pass #TODO: Continue from here tomorrow


@voters.post("/")
@voters.doc(
    summary="Voter Cast Vote",
    description="An endpoint for the voter to cast his vote in a mini election",
)
def voter_cast_vote():
    # Check if user has the right priveleges
    # Check if voter has already voted
    pass


@voters.post("/logout")
@voters.doc(summary="Voter Logout", description="An endpoint for the voter to logout")
def voter_logout():
    pass


############################################
##                 VOTER GROUP            ##
############################################
@voters.post("/groups")
@voters.doc(
    summary="Create Voter Group",
    description="An endpoint for the administrator to create a voter group",
)
def voter_group_create():
    pass


@voters.get("/groups")
@voters.doc(
    summary="Get Voter Group By Id",
    description="An endpoint to get the voter group by ID",
)
def voter_group_get_by_id():
    pass


@voters.get("/groups/all")
@voters.doc(
    summary="Get All Voter Groups", description="An endpoint to get all voter groups "
)
def voter_group_get_all():
    pass


@voters.delete("/groups")
@voters.doc(
    summary="Delete Voter Group",
    description="An endpoint for the administrator to delete a voter group",
)
def voter_group_delete():
    pass


@voters.put("/groups")
@voters.doc(
    summary="Modify Voter Group",
    description="An endpoint for the administrator to modify a voter group",
)
def voter_group_modify():
    pass
