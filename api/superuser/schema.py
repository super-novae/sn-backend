from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length, Regexp


class SuperUserSchema(Schema):
    auth_token = String(required=True)


class SuperuserLoginSchema(Schema):
    username = String(required=True, validate=[Length(min=4, max=15)])
    password = String(
        required=True,
        validate=[
            Length(min=8, max=16),
        ],
        metadata={
            "description": """
            * Password should contain at least one lowercase letter\n
            * Password should contain at least one uppercase letter\n
            * Password should contain at least one special character [!@#$%^&*()_+-=]\n
            * Password should have a minimum length of 8 and a maximum length of 16
            """
        },
    )

# Regexp(
#     "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+-=])[A-Za-z\d!@#$%^&*()_+-=]{8,}$"
# ),