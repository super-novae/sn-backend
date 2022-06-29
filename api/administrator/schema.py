from apiflask import Schema
from apiflask.fields import String, Email, List, Nested


class AdministratorSchema(Schema):
    public_id = String(dump_only=True, required=True)
    name = String(required=True)
    username = String(required=True)
    email = Email(required=True)
    password = String(load_only=True, required=True)


class AdministratorsSchema(Schema):
    administrators = List(Nested(AdministratorSchema))


class AdministratorLoginInputSchema(Schema):
    email = Email(required=True, load_only=True)
    password = String(required=True, load_only=True)


class AdministratorLoginOutputSchema(Schema):
    auth_token = String(required=True, dump_only=True)
    email = Email(required=True)
    name = String(required=True)
    public_id = String(dump_only=True, required=True)
    username = String(required=True)
