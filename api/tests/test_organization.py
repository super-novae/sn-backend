from .setup import truncate_db_tables
from ..organization.models import Organization
from ..test_data.admin_data import administrator_login, administrator_signup
from ..test_data.organization_data import (
    organization_details,
    organization_get_test_instance,
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
    superuser = superuser_login(client)

    response = client.post(
        "/api/v1/organization/",
        json=organization_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["id"][:4] == "org-"


def test_organization_create_not_authorized(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    administrator = administrator_login(client)

    response = client.post(
        "/api/v1/organization/",
        json=organization_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
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
    organization = organization_create()
    organization_name = organization.name
    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/organization/{organization.id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    modified_organization = Organization.find_by_id(
        organization.id
    )

    assert response.status_code == 200
    assert response.json["id"] == modified_organization.id
    assert organization_name != modified_organization.name


def test_organization_modify_by_id_non_existent(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/organization/org-some-random-public-key-onlin",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Organization with the given ID does not exists"


def test_organization_modify_by_id_not_authorized(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    administrator = administrator_login(client)
    organization = organization_create()

    response = client.put(
        f"/api/v1/organization/{organization.id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
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
    organization = organization_create()
    superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/organization/{organization.id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )
    
    deleted_organization = Organization.find_by_id(
        organization.id
    )


    assert response.status_code == 200
    assert (
        response.json["message"]
        == f"Organization <{organization.id}> deleted successfully."
    )
    assert deleted_organization == None


def test_organization_delete_by_id_non_existent(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/organization/org-some-random-public-key-onlin",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Organization with the given ID does not exists"


def test_organization_delete_by_id_not_authorized(client):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client)
    organization = organization_create()
    administrator = administrator_login(client)

    response = client.delete(
        f"/api/v1/organization/{organization.id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )
