from .errors import (
    VoterDoesNotExist,
    VoterAlreadyExists,
    VoterOrganizationIdNotProvided,
    VoterHasAlreadyVoted,
    VoterWrongCredentials,
)
from .models import Voter, Vote
from .schema import (
    VoterElections,
    VoterLoginInputSchema,
    VoterSchema,
    VotersSchema,
    VoterGetAllInputSchema,
    VoteSchema,
)
from apiflask import APIBlueprint
from api.election.models import Election
from api.extensions import db, logger
from api.generic.errors import UserDoesNotHaveRequiredRoles, InternalServerError
from api.generic.methods import has_roles
from api.generic.responses import GenericMessage
from api.organization.errors import OrganizationNotFound
from api.organization.models import Organization
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

voters = APIBlueprint("voter", __name__, tag="Voter", url_prefix="/api/v1/voters")


@voters.post("/signup")
@voters.input(VoterSchema)
@voters.output(VoterSchema)
@voters.doc(
    summary="Voter Signup",
    description="An endpoint for voter signup",
    responses=[201, 403, 409],
)
@jwt_required()
def voter_signup(data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    voter_email_exists = Voter.find_by_email(data["email"])

    if voter_email_exists:
        raise VoterAlreadyExists

    voter = Voter(**data)
    voter.password = data["password"]

    db.session.add(voter)
    db.session.commit()

    return voter, 201


@voters.post("/signup-bulk")
@voters.input(VotersSchema)
@voters.output(GenericMessage)
@voters.doc(
    summary="Voter Signup (Bulk)",
    description="An endpoint for bulk voter signup",
    responses=[201, 403],
)
@jwt_required()
def voter_bulk_signup(data):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    total_number_of_voters = len(data["voters"])

    try:
        for _, details in enumerate(data["voters"]):
            voter = Voter(**details)
            voter.password = details["password"]

            db.session.add(voter)
            db.session.flush()

        db.session.commit()

        return {"message": f"{total_number_of_voters} voters created successfully"}, 200

    except Exception as e:
        logger.info(e)
        raise InternalServerError


@voters.post("/login")
@voters.input(VoterLoginInputSchema)
@voters.output(VoterSchema)
@voters.doc(
    summary="Voter Login",
    description="An endpoint for voter login",
    responses=[200, 404],
)
def voter_login(data):
    voter: Voter = Voter.find_by_email(data["email"])

    if voter:
        voter_password_is_correct = voter.verify_password(data["password"])
        if voter_password_is_correct:
            voter.auth_token = create_access_token(voter.id)
            return voter, 200
    raise VoterWrongCredentials


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

    voter = Voter.find_by_id(voter_id)
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
    responses=[200, 400, 403, 404],
)
@jwt_required()
def voter_get_all(query):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    organization_id = query.get("organization_id", None)

    if organization_id:
        organization = Organization.find_by_id(organization_id)
        if organization:
            voters = Voter.find_all_organization_id(organization.id)

            return {"voters": voters}, 200
        raise OrganizationNotFound
    raise VoterOrganizationIdNotProvided


@voters.get("/<voter_id>/elections")
@voters.output(VoterElections)
@voters.doc(
    summary="Voter Elections",
    description="An endpoint to get all elections for voter",
    responses=[200, 403],
)
@jwt_required()
def voter_get_elections(voter_id):
    # Perform security checks
    user_has_required_roles = has_roles(["voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    voter: Voter = Voter.find_by_id(voter_id)
    src_elections = Election.find_by_type("SRC")
    college_elections = Election.find_by_college(voter.college)
    department_elections = Election.find_by_programme(voter.programme)

    return {
        "src_elections": src_elections,
        "college_elections": college_elections,
        "department_elections": department_elections,
    }, 200


@voters.post("/<voter_id>/vote")
@voters.input(VoteSchema)
@voters.output(VoteSchema)
@voters.doc(
    summary="Voter Cast Vote",
    description="An endpoint for the voter to cast his vote in a mini election",
    responses=[201, 400, 403],
)
@jwt_required()
def voter_cast_vote(voter_id, data):
    user_has_required_roles = has_roles(["voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    voter_has_already_voted = Vote.voter_vote_exists(
        data["voter_id"], data["office_id"]
    )
    if voter_has_already_voted:
        raise VoterHasAlreadyVoted

    vote = Vote(**data)

    db.session.add(vote)
    db.session.commit()

    return vote, 201


@voters.post("/logout")
@voters.doc(summary="Voter Logout", description="An endpoint for the voter to logout")
def voter_logout():
    pass


# TODO: [Future] Update Bulk Student Data
