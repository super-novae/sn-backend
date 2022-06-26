from apiflask import Schema
from apiflask.fields import DateTime, Email, String


class SuperUserSchema(Schema):
    public_id = String(required=True)
    name = String(required=True)
    username = String(required=True)
    email = Email(required=True)
    date_created = DateTime(required=True)
    auth_token = String(required=True)


class SuperuserLoginSchema(Schema):
    username = String(required=True)
    password = String(required=True)
