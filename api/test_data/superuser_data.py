from api.extensions import fake, db
from api.superuser.models import Superuser

data = {
    "email": fake.email(),
    "name": fake.name(),
    "password": fake.password(length=15),
    "username": fake.user_name()[:8],
}


def superuser_create():
    su = Superuser(**data)
    su.password = data["password"]

    db.session.add(su)
    db.session.commit()

    return su


def superuser_login(client):
    superuser_create()
    response = client.post(
        "/api/v1/superuser/login", json=superuser_login_correct_credentials()
    )

    return response.json

def superuser_signup_correct_credentials():
    return data

def superuser_login_correct_credentials():
    return {"username": data["username"], "password": data["password"]}


def superuser_login_wrong_credentials():
    return {"username": data["username"], "password": data["password"] + "goof"}
