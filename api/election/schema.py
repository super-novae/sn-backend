from apiflask import Schema
from apiflask.fields import String, List, Nested
from apiflask.validators import Length


class ElectionSchema(Schema):
    name = String(validate=[Length(5, 100)])


class ElectionsSchema(Schema):
    elections = List(Nested(ElectionSchema))


class CandidateSchema(Schema):
    name = String(validate=[Length(5, 80)])
    public_id = String(validate=[Length(equal=16)], dump_only=True)
    organization_id = String(validate=[Length(equal=28)])
    election_id = String(validate=[Length(equal=32)])


class CandidatesSchema(Schema):
    candidates = List(Nested(CandidateSchema))
