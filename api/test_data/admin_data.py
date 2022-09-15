from api.extensions import fake, db
from api.administrator.models import Administrator
from .superuser_data import superuser_login
from ..generic.password import generate_password
import random

data = {
    "email": fake.email(),
    "name": fake.name(),
    "username": fake.user_name()[:8],
}


def administrator_signup(client, seed=None):
    # Seed random function
    if seed:
        random.seed(seed)

    superuser_login(client)

    admin_details = administrator_signup_correct_credentials()

    admin = Administrator(**admin_details)
    admin.password = generate_password()

    db.session.add(admin)
    db.session.commit()

    return admin


def administrator_signup_correct_credentials():
    return data


def administrator_signup_username_exists():
    return {
        "email": fake.email(),
        "name": fake.name(),
        "username": data["username"],
    }


# "password": fake.password(length=15),


def administrator_signup_email_exists():
    return {
        "email": data["email"],
        "name": fake.name(),
        "username": fake.user_name()[:8],
    }


def administrator_modify():
    return {"name": fake.name(), "username": fake.user_name()[:8]}


def administrator_login(client, seed=None):
    if seed:
        random.seed(seed)

    response = client.post(
        "/api/v1/administrators/login",
        json=administrator_login_correct_credentials(),
    )

    return response.json


def administrator_login_correct_credentials(seed=None):
    if seed:
        random.seed(seed)
    return {"email": data["email"], "password": generate_password()}


def administrator_login_wrong_credentials(seed=None):
    if seed:
        random.seed(seed)
    return {"email": data["email"], "password": generate_password()[::-1]}


def administrator_get_test_instance() -> Administrator:
    return Administrator.find_by_email(data["email"])
