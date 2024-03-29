from .setup import truncate_db_tables
from ..administrator.models import Administrator
from ..test_data.admin_data import (
    administrator_login,
    administrator_login_correct_credentials,
    administrator_login_wrong_credentials,
    administrator_modify,
    administrator_signup,
    administrator_signup_correct_credentials,
    administrator_signup_email_exists,
    administrator_signup_username_exists,
)

from ..test_data.superuser_data import *
from ..test_data.organization_data import (
    organization_create,
    organization_add_administrator,
)
from ..test_data.voter_data import voter_create, voter_login


def test_administrator_signup_successful(client):
    # Remove all data from database
    truncate_db_tables()

    # Create a logged in superuser instance
    superuser_create()
    logged_in_superuser = superuser_login(client)

    # Create a request and store the response
    response = client.post(
        "/api/v1/administrators/signup",
        json=administrator_signup_correct_credentials(),
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    # Created administrator
    created_administrator: Administrator = Administrator.find_by_email(
        administrator_signup_correct_credentials()["email"]
    )

    # Perform required checks
    assert response.status_code == 201
    assert (
        response.json["email"]
        == administrator_signup_correct_credentials()["email"]
    )
    assert (
        response.json["name"]
        == administrator_signup_correct_credentials()["name"]
    )
    assert (
        response.json["username"]
        == administrator_signup_correct_credentials()["username"]
    )
    assert response.json["id"] == created_administrator.id


def test_administrator_signup_username_exists(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    logged_in_superuser = superuser_login(client)

    # Create a request and store the response
    response = client.post(
        "/api/v1/administrators/signup",
        json=administrator_signup_username_exists(),
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    # Perform required checks
    assert response.status_code == 409
    assert (
        response.json["message"]
        == "Administrator with this username already exists."
    )


def test_administrator_signup_email_exists(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    logged_in_superuser = superuser_login(client)

    # Create a request and store the response
    response = client.post(
        "/api/v1/administrators/signup",
        json=administrator_signup_email_exists(),
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    # Perform required checks
    assert response.status_code == 409
    assert (
        response.json["message"]
        == "Administrator with this email already exists."
    )


def test_administrator_signup_unauthorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    superuser_create()
    administrator_signup(client, seed)
    administrator = administrator_login(client, seed)

    response = client.post(
        "/api/v1/administrators/signup",
        json=administrator_signup_email_exists(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_administrator_modify_successful(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator = administrator_signup(client)
    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/administrators/{administrator.id}",
        json=administrator_modify(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Administrator modified successfully"


def test_administrator_modify_id_non_existent(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator = administrator_signup(client)
    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/administrators/{administrator.id[:6] + administrator.id[6:][::-1]}",
        json=administrator_modify(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )
    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Administrator with the given Id does not exist"
    )


def test_administrator_modify_unauthorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    superuser_login(client)
    administrator = administrator_login(client, seed)

    response = client.put(
        f"/api/v1/administrators/{administrator['id']}",
        json=administrator_modify(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_administrator_delete_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    superuser = superuser_login(client)
    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/administrators/{administrator['id']}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Administrator deleted successfully"


def test_administrator_delete_id_non_existent(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    superuser = superuser_login(client)
    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/administrators/{administrator['id'][:6] + administrator['id'][6:][::-1]}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Administrator with the given Id does not exist"
    )


def test_administrator_delete_unauthorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    superuser_login(client)
    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/administrators/{administrator['id'][:6] + administrator['id'][6:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_administrator_login_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    created_administrator = administrator_signup(client, seed)

    # Create a request and store the response
    response = client.post(
        "/api/v1/administrators/login",
        json=administrator_login_correct_credentials(seed),
    )

    assert response.status_code == 200
    assert (
        response.json["email"]
        == administrator_login_correct_credentials()["email"]
    )
    assert response.json["name"] == created_administrator.name
    assert response.json["id"] == created_administrator.id
    assert response.json["username"] == created_administrator.username
    assert response.json["auth_token"]


def test_administrator_login_wrong_credentials(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)

    # Create a request and store the response
    response = client.post(
        "/api/v1/administrators/login",
        json=administrator_login_wrong_credentials(seed),
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Administrator with the given credentials does not exist."
    )


def test_administrator_get_all_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    created_administrator = administrator_signup(client, seed)
    logged_in_superuser = superuser_login(client)

    # Create a request and store the response
    response = client.get(
        "/api/v1/administrators/",
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert (
        response.json["administrators"][0]["email"]
        == created_administrator.email
    )
    assert (
        response.json["administrators"][0]["name"]
        == created_administrator.name
    )
    assert response.json["administrators"][0]["id"] == created_administrator.id
    assert (
        response.json["administrators"][0]["username"]
        == created_administrator.username
    )


def test_administrator_get_all_not_authorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    logged_in_administrator = administrator_login(client, seed)

    # Create a request and store the response
    response = client.get(
        "/api/v1/administrators/",
        headers={
            "Authorization": f"Bearer {logged_in_administrator['auth_token']}"
        },
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_administrator_get_by_id_successful_admin(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    admin = administrator_signup(client, seed)
    logged_in_superuser = superuser_login(client)

    # Create a request and store the response
    response = client.get(
        f"/api/v1/administrators/{admin.id}",
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    assert response.status_code == 200
    assert response.json["email"] == admin.email
    assert response.json["name"] == admin.name
    assert response.json["id"] == admin.id
    assert response.json["username"] == admin.username


def test_administrator_get_by_id_successful_superuser(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    created_administrator = administrator_signup(client, seed)
    logged_in_superuser = superuser_login(client)

    # Create a request and store the response
    response = client.get(
        f"/api/v1/administrators/{created_administrator.id}",
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    assert response.status_code == 200
    assert response.json["email"] == created_administrator.email
    assert response.json["name"] == created_administrator.name
    assert response.json["id"] == created_administrator.id
    assert response.json["username"] == created_administrator.username


def test_administrator_get_by_id_non_existent(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    created_administrator = administrator_signup(client, seed)
    logged_in_superuser = superuser_login(client)

    # Create a request and store the response
    response = client.get(
        f"/api/v1/administrators/{created_administrator.id + 'goof'}",
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Administrator with the given credentials does not exist."
    )


def test_administrator_get_by_id_not_authorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    admin = administrator_signup(client, seed)
    organization_create()
    voter_create(seed)

    voter = voter_login(client, seed)

    # Create a request and store the response
    response = client.get(
        f"/api/v1/administrators/{admin.id}",
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_administrator_get_organization_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    admin = administrator_signup(client, seed)
    organization_create()
    organization_add_administrator()
    voter_create(seed)

    logged_in_superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/administrators/{admin.id}/org",
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    assert response.status_code == 200
    assert response.json["administrator_id"]
    assert response.json["id"]
    assert response.json["name"]


def test_administrator_get_organization_unauthorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    admin = administrator_signup(client, seed)
    organization_create()
    organization_add_administrator()
    voter_create(seed)

    voter = voter_login(client, seed)

    response = client.get(
        f"/api/v1/administrators/{admin.id}/org",
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_administrator_get_organization_organization_not_found(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    admin = administrator_signup(client, seed)
    organization_create()
    voter_create(seed)

    logged_in_superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/administrators/{admin.id}/org",
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Organization with the given ID does not exists"
    )


def test_administrator_get_organization_admin_not_found(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    admin = administrator_signup(client, seed)
    organization_create()
    organization_add_administrator()
    voter_create(seed)

    logged_in_superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/administrators/{admin.id[:6] + admin.id[6:][::-1]}/org",
        headers={
            "Authorization": f"Bearer {logged_in_superuser['auth_token']}"
        },
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Administrator with the given Id does not exist"
    )
