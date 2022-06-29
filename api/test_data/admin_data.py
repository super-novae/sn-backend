from api.extensions import fake

data = {
    "email": fake.email(),
    "name": fake.name(),
    "password": fake.password(length=15),
    "username": fake.user_name()[:8],
}


def administrator_signup(client):
    # API Call to create a new administrator
    response = client.post(
        "/api/v1/administrators/signup", json=administrator_signup_correct_credentials()
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
    administrator_signup(client)
    response = client.post(
        "/api/v1/administrators/login", json=administrator_login_correct_credentials()
    )

    return response.json


def administrator_login_correct_credentials():
    return {"email": data["email"], "password": data["password"]}


def administrator_login_wrong_credentials():
    return {"email": data["email"], "password": data["password"] + "goof"}
