from apiflask import Schema
from apiflask.fields import String, Integer, Email, Date, List, Nested
from apiflask.validators import Length, OneOf, Regexp
from api.generic.data import colleges
from api.election.schema import ElectionSchema
from api.generic.data import programmes, years


class VoterSchema(Schema):
    id = String(required=True, dump_only=True)
    student_id = String(required=True, validate=[Length(8)])
    name = String(required=True, validate=[Length(min=2, max=80)])
    username = String(required=True, validate=[Length(min=3, max=15)], dump_only=True)
    email = Email(required=True)
    telephone_number = String(required=True, validate=[Length(equal=10)])
    college = String(required=True, validate=[OneOf(colleges)])
    programme = String(required=False, validate=[OneOf(programmes)])
    year = String(
        required=True,
        validate=[
            OneOf(
                choices=years,
                error="Select a valid year",
            )
        ],
    )
    date_created = Date(required=True, dump_only=True)
    organization_id = String(required=True, validate=[Length(equal=32)])
    auth_token = String(dump_only=True)
    password = String(load_only=True, required=True)


class VotersSchema(Schema):
    voters = List(Nested(VoterSchema))


class VoterLoginInputSchema(Schema):
    email = Email(required=True)
    password = String(required=True)


class VoterGetAllInputSchema(Schema):
    organization_id = String(required=True, validate=[Length(equal=32)])


class VoterElections(Schema):
    src_elections = List(Nested(ElectionSchema))
    college_elections = List(Nested(ElectionSchema))
    department_elections = List(Nested(ElectionSchema))


class VoteSchema(Schema):
    id = Integer(dump_only=True)
    voter_id = String(required=True, validate=[Length(equal=32), Regexp("^voter-")])
    election_id = String(required=True, validate=[Length(equal=32), Regexp("^elec-")])
    candidate_id = String(validate=[Length(equal=32), Regexp("^cand-")])
    office_id = String(required=True, validate=[Length(equal=32), Regexp("^off-")])
