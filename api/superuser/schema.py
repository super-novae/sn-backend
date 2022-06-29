from apiflask import Schema
from apiflask.fields import String


class SuperUserSchema(Schema):
    auth_token = String(required=True)


class SuperuserLoginSchema(Schema):
    username = String(required=True)
    password = String(required=True)
