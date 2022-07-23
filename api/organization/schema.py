from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length


class OrganizationSchema(Schema):
    administrator_id = String(required=True, validate=[Length(equal=32)])
    name = String(required=True, validate=[Length(4, 256)])
    id = String(required=True, dump_only=True, validate=[Length(32)])

class OrganizationModifySchema(Schema):
    name = String(required=True, validate=[Length(4, 256)])
