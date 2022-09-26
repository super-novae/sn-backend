from .errors import (
    CandidateDoesNotExist,
    ElectionDoesNotExist,
    OfficeDoesNotExist,
)
from .models import Candidate, Election, Office
from .schema import (
    CandidateSchema,
    CandidatesSchema,
    ElectionSchema,
    ElectionStartEndSchema,
    ElectionsSchema,
    ElectionUpdateSchema,
    ElectionFullDetailsSchema,
    OfficeSchema,
    OfficesSchema,
    OfficeUpdateSchema,
)
from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.generic.errors import UserDoesNotHaveRequiredRoles
from api.generic.db import delete, modify, save
from api.generic.methods import has_roles, security_headers
from api.generic.responses import GenericMessage
from typing import List

election = APIBlueprint(
    "election", __name__, tag="Election", url_prefix="/api/v1/elections"
)


@election.post("/")
@election.input(ElectionSchema)
@election.output(ElectionSchema)
@election.doc(
    summary="Election Create",
    description="An endpoint for the creation of an election\n\nRoles: ADMIN",
    responses=[201, 403],
)
@jwt_required()
def election_create(data):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election(**data)

    election, error = save(election)

    if not error:
        return election, 201, security_headers


@election.put("/<election_id>")
@election.input(ElectionUpdateSchema)
@election.output(GenericMessage)
@election.doc(
    summary="Election modify",
    description="An endpoint to modify an election\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_modify(election_id, data):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(election_id)

    if not election:
        raise ElectionDoesNotExist

    for attribute, value in data.items():
        setattr(election, attribute, value)

    election, error = modify(election)

    if not error:
        return {"message": "Election modified successfully"}, 200


@election.delete("/<election_id>")
@election.output(GenericMessage)
@election.doc(
    summary="Election Delete",
    description="An endpoint to delete an election\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_delete(election_id):
    error = False

    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(election_id)

    if not election:
        raise ElectionDoesNotExist

    election, error = delete(election)

    if not error:
        return {"message": "Election deleted successfully"}, 200


@election.get("/<election_id>")
@election.output(ElectionSchema)
@election.doc(
    summary="Election Get by Id",
    description="An endpoint to get an election by Id\n\nRoles: ADMIN, VOTER",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_by_id(election_id):
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(election_id)

    if not election:
        raise ElectionDoesNotExist

    return election, 200


@election.get("/<election_id>/full_details")
@election.output(ElectionFullDetailsSchema)
@election.doc(
    summary="Election Get By Id (Full Details)",
    description="An endpoint to get an election and all related offices and candidates by id\n\nRoles: ADMIN, VOTER",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_by_id_full_details(election_id):
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(id=election_id)
    if not election:
        raise ElectionDoesNotExist

    offices: List[Office] = Office.find_all_by_election_id(
        election_id=election_id
    )

    office_candidate = []

    for office in offices:
        office_candidate.append(
            {
                "candidates": Candidate.find_all_candidates_by_office_id(
                    office_id=office.id
                ),
                "id": office.id,
                "name": office.name,
                "route_name": office.route_name,
            }
        )

    data = {"election": election, "offices": office_candidate}

    return data, 200


@election.get("/organization/<organization_id>")
@election.output(ElectionsSchema)
@election.doc(
    summary="Election Get All by Organization Id",
    description="An endpoint to get all elections by organization Id\n\nRoles: ADMIN",
    responses=[200, 403],
)
@jwt_required()
def election_get_all_by_organization_id(organization_id):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    elections = Election.find_all_elections_by_organization_id(
        organization_id=organization_id
    )

    return {"elections": elections}, 200


@election.post("/<election_id>/office/")
@election.input(OfficeSchema)
@election.output(OfficeSchema)
@election.doc(
    summary="Election Create Office",
    description="An endpoint to create an office in an election\n\nRoles: ADMIN",
    responses=[201, 403],
)
@jwt_required()
def election_create_office(election_id, data):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    office = Office(**data)

    office, error = save(office)

    if not error:
        return office, 201


@election.put("/<election_id>/office/<office_id>")
@election.input(OfficeUpdateSchema)
@election.output(GenericMessage)
@election.doc(
    summary="Election Modify Office",
    description="An endpoint to modify an office in an election\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_modify_office(election_id, office_id, data):
    error = False

    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    office = Office.find_by_id(id=office_id)

    if not office:
        raise OfficeDoesNotExist

    for attribute, value in data.items():
        setattr(office, attribute, value)

    office, error = modify(office)

    if not error:
        return {"message": "Office modified successfully"}, 200


@election.delete("/<election_id>/office/<office_id>")
@election.output(GenericMessage)
@election.doc(
    summary="Election Delete Office",
    description="An endpoint to delete an office in an election\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_delete_office(election_id, office_id):
    error = False

    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    office = Office.find_by_id(id=office_id)

    if not office:
        raise OfficeDoesNotExist

    office, error = delete(office)

    if not error:
        return {"message": "Office deleted successfully"}, 200


@election.get("/<election_id>/office/<office_id>")
@election.output(OfficeSchema)
@election.doc(
    summary="Election Get Office By Id",
    description="An endpoint to get an office by id in an election\n\nRoles: ADMIN, VOTER",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_office_by_id(election_id, office_id):
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    office = Office.find_by_id(id=office_id)

    if not office:
        raise OfficeDoesNotExist

    return office, 200


@election.get("/<election_id>/office/")
@election.output(OfficesSchema)
@election.doc(
    summary="Election Get Office By Id",
    description="An endpoint to get all offices by election id\n\nRoles: ADMIN, VOTER",
    responses=[200, 403],
)
@jwt_required()
def election_get_all_offices_by_election_id(election_id):
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
    description="An endpoint to create a candidate in election\n\nRoles: ADMIN",
    responses=[201, 403],
)
@jwt_required()
def election_create_candidate(election_id, data):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate = Candidate(**data)

    candidate, error = save(candidate)

    if not error:
        return candidate, 201


@election.put("/<election_id>/candidates/<candidate_id>")
@election.input(ElectionUpdateSchema)
@election.output(GenericMessage)
@election.doc(
    summary="Election Modify Candidate",
    description="An endpoint to modify a candidate in election\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_modify_candidate(election_id, candidate_id, data):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate = Candidate.find_candidate_by_id(
        id=candidate_id, election_id=election_id
    )

    if not candidate:
        raise CandidateDoesNotExist

    for attribute, value in data.items():
        setattr(candidate, attribute, value)

    candidate, error = modify(candidate)

    if not error:
        return {"message": "Candidate modified successfully"}, 200


@election.delete("/<election_id>/candidates/<candidate_id>")
@election.output(GenericMessage)
@election.doc(
    summary="Election Delete Candidate",
    description="An endpoint to delete a candidate in election\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_delete_candidate(election_id, candidate_id):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate = Candidate.find_candidate_by_id(
        id=candidate_id, election_id=election_id
    )

    if not candidate:
        raise CandidateDoesNotExist

    candidate, error = delete(candidate)

    if not error:
        return {"message": "Candidate deleted successfully"}, 200


@election.get("/<election_id>/candidates/<candidate_id>")
@election.output(CandidateSchema)
@election.doc(
    summary="Election Get Candidate by Id",
    description="An endpoint to get candidate by Id\n\nRoles: ADMIN, VOTER",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_candidate_by_id(election_id, candidate_id):
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidate: Candidate = Candidate.find_candidate_by_id(
        id=candidate_id, election_id=election_id
    )

    if not candidate:
        raise CandidateDoesNotExist

    office: Office = Office.find_by_id(candidate.office_id)
    candidate.office_name = office.name

    return candidate, 200


@election.get("/<election_id>/candidates/")
@election.output(CandidatesSchema)
@election.doc(
    summary="Election Get Candidates by Election Id",
    description="An endpoint to get all candidates by election Id\n\nRoles: ADMIN, VOTER",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_all_candidates_by_election_id(election_id):
    user_has_required_roles = has_roles(["admin", "voter"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    candidates = Candidate.find_all_candidates_by_election_id(
        election_id=election_id
    )

    return {"candidates": candidates}, 200


@election.get("/<election_id>/office/<office_id>/candidates")
@election.output(CandidatesSchema)
@election.doc(
    summary="Election Get Candidates by Office Id",
    description="An endpoint to get all candidates by office id\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_get_all_candidate_by_office_id(election_id, office_id):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    office = Office.find_by_id(office_id)

    if office:
        candidates = Candidate.find_all_candidates_by_office_id(
            office_id=office_id
        )
        return {"candidates": candidates}, 200
    raise OfficeDoesNotExist


@election.post("/<election_id>/change/")
@election.input(ElectionStartEndSchema)
@election.output(GenericMessage)
@election.doc(
    summary="Election Start / End",
    description="An endpoint to start or end an election\n\nRoles: ADMIN",
    responses=[200, 403, 404],
)
@jwt_required()
def election_change_state(election_id, data):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())
    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election: Election = Election.find_by_id(id=election_id)
    if not election:
        raise ElectionDoesNotExist

    election.state = data["state"]

    election, error = modify(election)

    if not error:
        return {
            "message": f"Election {election.name} has been changed to {election.state}"
        }, 200
