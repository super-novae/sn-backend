from apiflask import Schema
from apiflask.fields import String, Integer, Nested, List
from apiflask.validators import Regexp, Length


class DataQuerySchema(Schema):
    organization_id = String(
        required=True, validate=[Regexp("^org-"), Length(equal=32)]
    )
    election_id = String(
        required=True, validate=[Regexp("^elec-"), Length(equal=32)]
    )


class OfficeWinnerSchema(Schema):
    candidate_name = String(required=True)
    total_votes = Integer(required=True)


class OfficeCandidateSchema(Schema):
    name = String(required=True)
    vote_count = Integer(required=True)


class OfficeResultSchema(Schema):
    office_name = String()
    candidates = List(Nested(OfficeCandidateSchema))
    total_vote_count = Integer(required=True)
    winner = Nested(OfficeWinnerSchema)


class ElectionResultSchema(Schema):
    results = List(Nested(OfficeResultSchema))
