from apiflask import Schema
from apiflask.fields import String, Email, Integer, DateTime, List, Nested


class AdministratorSchema(Schema):
    public_id = String(dump_only=True, required=True)
    name = String(required=True)
    username = String(required=True)
    email = Email(required=True)
    date_created = DateTime(required=True)
    password = String(load_only=True, required=True)


class AdministratorsSchema(Schema):
    administrators = List(Nested(AdministratorSchema))


class AdministratorLoginSchema(Schema):
    username = String(required=True, load_only=True)
    password = String(required=True, load_only=True)
