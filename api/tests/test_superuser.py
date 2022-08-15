from .setup import truncate_db_tables
from api.test_data.superuser_data import (
    superuser_create,
    superuser_login_correct_credentials,
    superuser_login_wrong_credentials,
)


def test_superuser_login_successful(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()

    # Create a request and store the response
    response = client.post(
        "/api/v1/superuser/login", json=superuser_login_correct_credentials()
    )

    assert response.status_code == 200
    assert response.json["auth_token"]

    # Clear database after tests
    truncate_db_tables()


def test_super_user_login_wrong_credentials(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()

    # Create a request and store the response
    response = client.post(
        "/api/v1/superuser/login", json=superuser_login_wrong_credentials()
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Superuser with the given credentials does not exist"
    )

    # Clear database after tests
    truncate_db_tables()
