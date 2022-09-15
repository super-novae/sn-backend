from .errors import (
    VoterDoesNotExist,
    VoterAlreadyExists,
    VoterHasAlreadyVoted,
    VoterWrongCredentials,
)
from .models import Voter, Vote
from .schema import (
    VoterElections,
    VoterLoginInputSchema,
    VoterRecoverAccountSchema,
    VoterSchema,
    VotersSchema,
    VoterGetAllInputSchema,
    VoteSchema,
)
from apiflask import APIBlueprint, abort
from api.election.models import Election
from api.extensions import db, logger
from api.generic.db import save, modify
from api.generic.errors import (
    UserDoesNotHaveRequiredRoles,
)
from api.generic.mail import send_password_to_voter
from api.generic.methods import has_roles
from api.generic.password import generate_password
from api.generic.responses import GenericMessage
from api.organization.errors import OrganizationNotFound
from api.organization.models import Organization
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from sys import exc_info

voters = APIBlueprint(
    "voter", __name__, tag="Voter", url_prefix="/api/v1/voters"
)


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

    password = generate_password()

    voter.password = password

    send_password_to_voter(data["email"], data["name"], password)

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
    error = False

    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    total_number_of_voters = len(data["voters"])

    try:
        for _, details in enumerate(data["voters"]):
            voter = Voter(**details)
            password = generate_password()
            voter.password = password

            db.session.add(voter)
            db.session.flush()

            send_password_to_voter(details["email"], details["name"], password)

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
            "message": f"{total_number_of_voters} voters created successfully"
        }, 200


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
    examples=["/?organization_id=org-12c41vc41vc41v34123412341234"],
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
    description="An endpoint for the voter to cast his vote in an election",
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

    vote, error = save(vote)

    if not error:
        return vote, 201


# TODO: Implement voter logout
# @voters.post("/logout")
# @voters.doc(summary="Voter Logout", description="An endpoint for the voter to logout")
# def voter_logout():
#     pass


# TODO: [Future] Update Bulk Student Data


@voters.post("/password_reset")
@voters.input(VoterRecoverAccountSchema)
@voters.output(GenericMessage)
@voters.doc(
    summary="Voter Reset Password",
    description="An endpoint for the voter to reset her/his password",
    responses=[200, 400],
)
def voter_reset_password(data):
    voter = Voter.find_by_email(data["email"])
    if not voter:
        raise VoterDoesNotExist

    new_password = generate_password()
    voter.password = new_password
    voter, error = modify(voter)

    send_password_to_voter(voter.email, voter.name, new_password)

    if not error:
        return {"message": "A new password will be sent if the email exists"}
