from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length


class OrganizationSchema(Schema):
    administrator_id = Integer(required=True)
    name = String(required=True, validate=[Length(4, 256)])
    public_id = String(required=True, dump_only=True, validate=[Length(32)])

class OrganizationModifySchema(Schema):
    name = String(required=True, validate=[Length(4, 256)])
