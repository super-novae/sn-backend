from apiflask import Schema
from apiflask.fields import String, List, Nested
from apiflask.validators import Length, Regexp, URL


class ElectionSchema(Schema):
    name = String(validate=[Length(5, 100)], required=True)
    organization_id = String(required=True, validate=[Regexp("^org-"), Length(equal=32)])
    route_name = String(required=True, validate=[Length(min=4, max=50)])


class ElectionsSchema(Schema):
    elections = List(Nested(ElectionSchema))


class ElectionUpdateSchema(Schema):
    name = String(validate=[Length(5, 100)], required=True)
    route_name = String(required=False, validate=[Length(min=4, max=50)])


class OfficeSchema(Schema):
    id = String(required=True, dump_only=True)
    name = String(required=True)
    route_name = String(required=True, validate=[Length(min=4, max=50)])
    election_id = String(required=True, validate=[Regexp("^elec-"), Length(equal=32)])


class OfficesSchema(Schema):
    offices = List(Nested(OfficeSchema))
    

class OfficeUpdateSchema(Schema):
    name = String(required=True)
    route_name = String(required=True, validate=[Length(min=4, max=50)])
    

class CandidateSchema(Schema):
    name = String(validate=[Length(5, 80)], required=True)
    public_id = String(validate=[Length(equal=16)], dump_only=True)
    organization_id = String(validate=[Length(equal=32)])
    election_id = String(validate=[Length(equal=32)])
    profile_image_url = String(validate=[URL(schemes=["https"])])
    office_id = String(required=True, validate=[Regexp("^off-")])
    programme = String(required=True, validate=[Length(min=10, max=100)])


class CandidatesSchema(Schema):
    candidates = List(Nested(CandidateSchema))
