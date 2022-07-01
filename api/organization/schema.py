from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length


class OrganizationSchema(Schema):
    public_id = String(required=True, dump_only=True, validate=[Length(32)])
    name = String(required=True, validate=[Length(4, 256)])
