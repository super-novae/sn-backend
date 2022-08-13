import re
from apiflask import Schema
from apiflask.fields import String, Email, List, Nested


class AdministratorSchema(Schema):
    id = String(dump_only=True, required=True)
    name = String(required=True)
    username = String(required=True)
    email = Email(required=True)
    password = String(load_only=True, required=True)


class AdministratorModifySchema(Schema):
    name = String(required=False)
    username = String(required=False)
    email = String(required=False)


class AdministratorsSchema(Schema):
    administrators = List(Nested(AdministratorSchema))


class AdministratorLoginInputSchema(Schema):
    email = Email(required=True, load_only=True)
    password = String(required=True, load_only=True)


class AdministratorLoginOutputSchema(Schema):
    auth_token = String(required=True, dump_only=True)
    email = Email(required=True)
    name = String(required=True)
    id = String(dump_only=True, required=True)
    username = String(required=True)
