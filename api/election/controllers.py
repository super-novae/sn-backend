from .errors import (
    CandidateDoesNotExist, 
    ElectionDoesNotExist, 
    OfficeDoesNotExist)
from .models import Candidate, Election, Office
from .schema import (
    CandidateSchema,
    CandidatesSchema,
    ElectionSchema,
    ElectionsSchema,
    ElectionUpdateSchema,
    OfficeSchema,
    OfficesSchema,
    OfficeUpdateSchema
)
from api.extensions import db
from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.generic.errors import UserDoesNotHaveRequiredRoles
from api.generic.methods import has_roles
from api.generic.responses import GenericMessage

election = APIBlueprint(
    "election", __name__, tag="Election", url_prefix="/api/v1/elections"
)


@election.post("/")
@election.input(ElectionSchema)
@election.output(ElectionSchema)
@election.doc(
    summary="Election Create",
    description="An endpoint for the creation of an election",
    responses=[201, 403],
)
@jwt_required()
def election_create(data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election(**data)

    db.session.add(election)
    db.session.commit()

    return election, 201


@election.put("/<election_id>")
@election.input(ElectionUpdateSchema)
@election.output(GenericMessage)
@election.doc(
    summary="Election modify",
    description="An endpoint to modify an election",
    responses=[200, 403, 404],
)
@jwt_required()
def election_modify(election_id, data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(election_id)

    if not election:
        raise ElectionDoesNotExist

    for attribute, value in data.items():
        setattr(election, attribute, value)

    db.session.commit()

    return {"message": "Election modified successfully"}, 200


@election.delete("/<election_id>")
@election.output(GenericMessage)
@election.doc(
    summary="Election Delete",
    description="An endpoint to delete an election",
    responses=[200, 403, 404],
)
@jwt_required()
def election_delete(election_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(election_id)

    if not election:
        raise ElectionDoesNotExist

    db.session.delete(election)
    db.session.commit()

    return {"message": "Election deleted successfully"}, 200


@election.get("/<election_id>")
@election.output(ElectionSchema)
@election.doc(
    summary="Election Get by Id",
    description="An endpoint to get an election by Id",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_by_id(election_id):
    # Perform security checks
    user_has_required_roles = has_roles(
        ["admin"], get_jwt_identity()
    )  # TODO: Include voters
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(election_id)

    if not election:
        raise ElectionDoesNotExist

    return election, 200


@election.get("/organization/<organization_id>")
@election.output(ElectionsSchema)
@election.doc(
    summary="Election Get All by Organization Id",
    description="An endpoint to get all elections by organization Id",
    responses=[200, 403],
)
@jwt_required()
def election_get_all_by_organization_id(organization_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    elections = Election.find_all_elections_by_organization_id(
        organization_id=organization_id
    )

    return {"elections": elections}, 200


# TODO: Get all election by voter_id
# @election.get("/<election_id>/voter/<voter_id>")
# @jwt_required()
# def election_get_all_by_voter_id(election_id, voter_id):
#     elections = Election.find_all_elections_by_voter_id(voter_id=voter_id)

#     return {"elections": elections}

@election.post("/<election_id>/office/")
@election.input(OfficeSchema)
@election.output(OfficeSchema)
@election.doc(
    summary="Election Create Office",
    description="An endpoint to create an office in an election",
    responses=[201, 403],
)
@jwt_required()
def election_create_office(election_id, data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles
    
    office = Office(**data)
    
    db.session.add(office)
    db.session.commit()
    
    return office, 201

@election.put("/<election_id>/office/<office_id>")
@election.input(OfficeUpdateSchema)
@election.output(GenericMessage)
@election.doc(
    summary="Election Modify Office",
    description="An endpoint to modify an office in an election",
    responses=[200, 403, 404],
)
@jwt_required()
def election_modify_office(election_id, office_id, data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles
    
    office = Office.find_by_id(id=office_id)
    
    if not office:
        raise OfficeDoesNotExist
    
    for attribute, value in data.items():
        setattr(office, attribute, value)
    
    db.session.commit()
    
    return {"message": "Office modified successfully"}, 200

@election.delete("/<election_id>/office/<office_id>")
@election.output(GenericMessage)
@election.doc(
    summary="Election Delete Office",
    description="An endpoint to delete an office in an election",
    responses=[200, 403, 404],
)
@jwt_required()
def election_delete_office(election_id, office_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    office = Office.find_by_id(id=office_id)
    
    if not office:
        raise OfficeDoesNotExist
    
    db.session.delete(office)
    db.session.commit()
    
    return {"message": "Office deleted successfully"}, 200


@election.get("/<election_id>/office/<office_id>")
@election.output(OfficeSchema)
@election.doc(
    summary="Election Get Office By Id",
    description="An endpoint to get an office by id in an election",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_office_by_id(election_id, office_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles
    
    office = Office.find_by_id(id=office_id)
    
    if not office:
        raise OfficeDoesNotExist
    
    return office, 200

@election.post("/<election_id>/office/")
@election.output(OfficesSchema)
@election.doc(
    summary="Election Get Office By Id",
    description="An endpoint to get all offices by election id",
    responses=[200, 403],
)
@jwt_required()
def election_get_all_offices_by_election_id(election_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles
    
    offices = Office.find_all_by_election_id(election_id=election_id)
    
    return {"offices": offices}, 200


@election.post("/<election_id>/candidates/")
@election.input(CandidateSchema)
@election.output(CandidateSchema)
@election.doc(
    summary="Election Create Candidate",
    description="An endpoint to create a candidate in election",
    responses=[201, 403],
)
@jwt_required()
def election_create_candidate(election_id, data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate = Candidate(**data)

    db.session.add(candidate)
    db.session.commit()

    return candidate, 201


@election.put("/<election_id>/candidates/<candidate_id>")
@election.input(ElectionUpdateSchema)
@election.output(GenericMessage)
@election.doc(
    summary="Election Modify Candidate",
    description="An endpoint to modify a candidate in election",
    responses=[200, 403, 404],
)
@jwt_required()
def election_modify_candidate(election_id, candidate_id, data):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate = Candidate.find_candidate_by_id(id=candidate_id, election_id=election_id)

    if not candidate:
        raise CandidateDoesNotExist

    for attribute, value in data.items():
        setattr(candidate, attribute, value)

    db.session.commit()

    return {"message": "Candidate modified successfully"}, 200


@election.delete("/<election_id>/candidates/<candidate_id>")
@election.output(GenericMessage)
@election.doc(
    summary="Election Delete Candidate",
    description="An endpoint to delete a candidate in election",
    responses=[200, 403, 404],
)
@jwt_required()
def election_delete_candidate(election_id, candidate_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate = Candidate.find_candidate_by_id(id=candidate_id, election_id=election_id)

    if not candidate:
        raise CandidateDoesNotExist

    db.session.delete(candidate)
    db.session.commit()

    return {"message": "Candidate deleted successfully"}, 200


@election.get("/<election_id>/candidates/<candidate_id>")
@election.output(CandidateSchema)
@election.doc(
    summary="Election Get Candidate by Id",
    description="An endpoint to get candidate by Id",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_candidate_by_id(election_id, candidate_id):
    # Perform security checks
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate = Candidate.find_candidate_by_id(id=candidate_id, election_id=election_id)

    if not candidate:
        raise CandidateDoesNotExist

    return candidate, 200


@election.get("/<election_id>/candidates/")
@election.output(CandidatesSchema)
@election.doc(
    summary="Election Get Candidates by Election Id",
    description="An endpoint to get all candidates by election Id",
    responses=[200, 403],
)
@jwt_required()
def election_get_all_candidates_by_election_id(election_id):
    # Perform security checks
    # TODO: Add votor to user_has_required_roles
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidates = Candidate.find_all_candidates_by_election_id(election_id=election_id)

    return {"candidates": candidates}, 200
