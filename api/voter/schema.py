from apiflask import Schema
from apiflask.fields import String, Email, Date, List, Nested
from apiflask.validators import Length, OneOf


class VoterSchema(Schema):
    id = String(required=True, dump_only=True)
    student_id = String(required=True, validate=[Length(8)])
    name = String(required=True, validate=[Length(min=2, max=80)])
    username = String(required=True, validate=[Length(min=3, max=15)])
    email = Email(required=True)
    telephone = String(required=True, validate=[Length(equal=10)])
    programme = String(required=True, validate=[Length(min=10, max=100)])
    year = String(
        required=True,
        validate=[
            OneOf(
                choices=["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"],
                error="Select a valid year",
            )
        ],
    )
    date_created = Date(required=True, dump_only=True)
    organization_id = String(required=True, validate=[Length(equal=32)])
    auth_token = String(dump_only=True)


class VotersSchema(Schema):
    voters = List(Nested(VoterSchema))


class VoterGetAllInputSchema(Schema):
    organization_id = String(required=True, validate=[Length(equal=32)])
