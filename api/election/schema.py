from apiflask import Schema
from apiflask.fields import String, List, Nested, Boolean
from apiflask.validators import Length, Regexp, URL, OneOf
from api.generic.data import types, colleges, programmes


class ElectionSchema(Schema):
    id = String(required=True, dump_only=True)
    name = String(validate=[Length(5, 100)], required=True)
    organization_id = String(
        required=True, validate=[Regexp("^org-"), Length(equal=32)]
    )
    route_name = String(required=True, validate=[Length(min=4, max=50)])
    type = String(required=True, validate=[OneOf(types)])
    college = String(required=False, validate=[OneOf(colleges)])
    programme = String(required=False, validate=[OneOf(programmes)])
    state = Boolean(required=True, dump_only=True)


class ElectionsSchema(Schema):
    elections = List(Nested(ElectionSchema))


class ElectionUpdateSchema(Schema):
    name = String(validate=[Length(5, 100)], required=True)
    route_name = String(required=False, validate=[Length(min=4, max=50)])


class OfficeSchema(Schema):
    id = String(required=True, dump_only=True)
    name = String(required=True)
    route_name = String(required=True, validate=[Length(min=4, max=50)])
    election_id = String(
        required=True, validate=[Regexp("^elec-"), Length(equal=32)]
    )


class OfficesSchema(Schema):
    offices = List(Nested(OfficeSchema))


class OfficeUpdateSchema(Schema):
    name = String(required=True)
    route_name = String(required=True, validate=[Length(min=4, max=50)])


class CandidateSchema(Schema):
    name = String(validate=[Length(5, 80)], required=True)
    id = String(validate=[Length(equal=32)], dump_only=True)
    organization_id = String(validate=[Length(equal=32)])
    election_id = String(validate=[Length(equal=32)])
    profile_image_url = String(validate=[URL(schemes=["https"])])
    office_id = String(required=True, validate=[Regexp("^off-")])
    office_name = String(required=False)
    programme = String(required=True, validate=[Length(min=10, max=100)])


class CandidatesSchema(Schema):
    candidates = List(Nested(CandidateSchema))


class OfficeCandidates(Schema):
    id = String(required=True, dump_only=True)
    name = String(required=True)
    route_name = String(required=True, validate=[Length(min=4, max=50)])
    candidates = List(Nested(CandidateSchema))


class ElectionFullDetailsSchema(Schema):
    election = Nested(ElectionSchema)
    offices = List(Nested(OfficeCandidates))


class ElectionStartEndSchema(Schema):
    state = String(required=True, validate=[OneOf(["in-session", "on-hold"])])
