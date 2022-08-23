from apiflask import APIBlueprint
from api.election.models import Office, Candidate
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.election.models import Election
from api.election.errors import ElectionDoesNotExist
from api.generic.errors import UserDoesNotHaveRequiredRoles
from .schema import DataQuerySchema, ElectionResultSchema
from typing import List
from api.generic.methods import has_roles


data = APIBlueprint("data", __name__, tag="Data", url_prefix="/api/v1/data")


@data.get("/")
@data.input(DataQuerySchema, location="query", example="hello")
@data.output(ElectionResultSchema)
@jwt_required()
def data_get_election_results(query):
    user_has_required_roles = has_roles(["admin"], get_jwt_identity())

    if not user_has_required_roles:
        raise UserDoesNotHaveRequiredRoles

    election = Election.find_by_id(id=query.get("election_id"))
    if not election:
        raise ElectionDoesNotExist

    election_offices: List[Office] = Office.find_all_by_election_id(
        election_id=query.get("election_id")
    )

    data = []

    for index, office in enumerate(election_offices):
        data.append(
            {
                "office_name": office.name,
                "candidates": [],
                "total_vote_count": 0,
                "winner": {"total_votes": 0},
            }
        )

        candidate: Candidate
        for candidate in office.candidates:
            data[index]["candidates"].append(
                {
                    "name": candidate.name,
                    "vote_count": (vote_count := len(candidate.votes)),
                }
            )
            data[index]["total_vote_count"] += vote_count

            if vote_count > data[index]["winner"]["total_votes"]:
                data[index]["winner"] = {
                    "candidate_name": candidate.name,
                    "total_votes": vote_count,
                }

    return {"results": data}, 200
