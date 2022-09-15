from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length


class SuperUserSchema(Schema):
    auth_token = String(required=True)


class SuperuserLoginSchema(Schema):
    username = String(required=True, validate=[Length(min=4, max=15)])
    password = String(
        required=True,
        validate=[
            Length(min=8, max=16),
        ],
    )
