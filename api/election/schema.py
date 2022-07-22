from apiflask import Schema
from apiflask.fields import String, List, Nested, Integer
from apiflask.validators import Length, Regexp, URL


class ElectionSchema(Schema):
    name = String(validate=[Length(5, 100)], required=True)
    organization_id = String(required=True, validate=[Regexp("^org-")])


class ElectionsSchema(Schema):
    elections = List(Nested(ElectionSchema))


class ElectionUpdateSchema(Schema):
    name = String(validate=[Length(5, 100)], required=True)


class CandidateSchema(Schema):
    name = String(validate=[Length(5, 80)], required=True)
    public_id = String(validate=[Length(equal=16)], dump_only=True)
    organization_id = String(validate=[Length(equal=28)])
    election_id = String(validate=[Length(equal=32)])
    profile_image_url = String(validate=[URL(schemes=["https"])])


class CandidatesSchema(Schema):
    candidates = List(Nested(CandidateSchema))
