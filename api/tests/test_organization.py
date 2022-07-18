from .setup import truncate_db_tables
from ..organization.models import Organization
from ..test_data.admin_data import administrator_login, administrator_signup
from ..test_data.organization_data import (
    organization_details,
    organization_modified_details,
    organization_create,
)
from ..test_data.superuser_data import superuser_create, superuser_login


def test_organization_create_successful(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    logged_in_superuser = superuser_login(client)

    response = client.post(
        "/api/v1/organization/",
        json=organization_details(),
        headers={"Authorization": f"Bearer {logged_in_superuser['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["public_id"][:4] == "org-"


def test_organization_create_not_authorized(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    logged_in_administrator = administrator_login(client)


    response = client.post(
        "/api/v1/organization/",
        json=organization_details(),
        headers={"Authorization": f"Bearer {logged_in_administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_organization_modify_by_id_successful(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    created_organization = organization_create()
    created_organization_name = created_organization.name
    logged_in_superuser = superuser_login(client)
    
    response = client.put(
        f"/api/v1/organization/{created_organization.public_id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {logged_in_superuser['auth_token']}"},
    )

    modified_organization = Organization.find_by_public_id(
        created_organization.public_id
    )

    assert response.status_code == 200
    assert response.json["public_id"] == modified_organization.public_id
    assert created_organization_name != modified_organization.name


def test_organization_modify_by_id_non_existent(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    logged_in_superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/organization/org-some-random-public-key-onlin",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {logged_in_superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Organization with the given ID does not exists"


def test_organization_modify_by_id_not_authorized(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    logged_in_administrator = administrator_login(client)
    created_organization = organization_create()

    response = client.put(
        f"/api/v1/organization/{created_organization.public_id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {logged_in_administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_organization_delete_by_id_successful(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    created_organization = organization_create()
    created_organization_public_id = created_organization.public_id
    logged_in_superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/organization/{created_organization_public_id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {logged_in_superuser['auth_token']}"},
    )

    deleted_organization = Organization.find_by_public_id(
        created_organization_public_id
    )

    assert response.status_code == 200
    assert (
        response.json["message"]
        == f"Organization <{created_organization_public_id}> deleted successfully."
    )
    assert deleted_organization == None


def test_organization_delete_by_id_non_existent(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    logged_in_superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/organization/org-some-random-public-key-onlin",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {logged_in_superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Organization with the given ID does not exists"


def test_organization_delete_by_id_not_authorized(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    created_organization = organization_create()
    created_organization_public_id = created_organization.public_id
    logged_in_administrator = administrator_login(client)

    response = client.delete(
        f"/api/v1/organization/{created_organization_public_id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {logged_in_administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )
