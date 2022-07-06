from apiflask import Schema
from apiflask.fields import String


class GenericMessage(Schema):
    message = String()
