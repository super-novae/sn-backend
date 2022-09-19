from apiflask import Schema
from apiflask.fields import String, Nested, List
from apiflask.validators import Length, Regexp


class OrganizationSchema(Schema):
    administrator_id = String(
        required=True,
        validate=[Length(equal=32), Regexp("^admin-")],
        dump_only=True,
    )
    name = String(required=True, validate=[Length(4, 256)])
    id = String(required=True, dump_only=True, validate=[Length(32)])


class OrganizationModifySchema(Schema):
    name = String(required=True, validate=[Length(4, 256)])


class OrganizationsSchema(Schema):
    organizations = List(Nested(OrganizationSchema))


class OrganizationAdminSchema(Schema):
    administrator_id = String(
        required=True, validate=[Length(equal=32), Regexp("^admin-")]
    )
