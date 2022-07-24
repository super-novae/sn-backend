from api.extensions import fake
from api.administrator.models import Administrator
from .superuser_data import superuser_login

data = {
    "email": fake.email(),
    "name": fake.name(),
    "password": fake.password(length=15),
    "username": fake.user_name()[:8],
}


def administrator_signup(client):
    logged_in_superuser = superuser_login(client)

    response = client.post(
        "/api/v1/administrators/signup",
        json=administrator_signup_correct_credentials(),
        headers={"Authorization": f"Bearer {logged_in_superuser['auth_token']}"},
    )

    return response.json


def administrator_signup_correct_credentials():
    return data


def administrator_signup_username_exists():
    return {
        "email": fake.email(),
        "name": fake.name(),
        "password": fake.password(length=15),
        "username": data["username"],
    }


def administrator_signup_email_exists():
    return {
        "email": data["email"],
        "name": fake.name(),
        "password": fake.password(length=15),
        "username": fake.user_name()[:8],
    }


def administrator_login(client):
    response = client.post(
        "/api/v1/administrators/login", json=administrator_login_correct_credentials()
    )

    return response.json


def administrator_login_correct_credentials():
    return {"email": data["email"], "password": data["password"]}


def administrator_login_wrong_credentials():
    return {"email": data["email"], "password": data["password"] + "goof"}


def administrator_get_test_instance() -> Administrator:
    return Administrator.find_by_email(data["email"])
