from .setup import truncate_db_tables
from ..organization.models import Organization
from ..test_data.admin_data import administrator_login, administrator_signup
from ..test_data.organization_data import (
    organization_details,
    organization_modified_details,
    organization_create,
)
from ..test_data.superuser_data import superuser_create, superuser_login


def test_organization_create_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    superuser = superuser_login(client)

    response = client.post(
        "/api/v1/organization/",
        json=organization_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 201
    assert response.json["id"][:4] == "org-"

    # Clear database after tests
    truncate_db_tables()


def test_organization_create_not_authorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    administrator = administrator_login(client, seed)

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

    # Clear database after tests
    truncate_db_tables()


def test_organization_modify_by_id_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    organization_name = organization.name
    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/organization/{organization.id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    modified_organization = Organization.find_by_id(organization.id)

    assert response.status_code == 200
    assert response.json["id"] == modified_organization.id
    assert organization_name != modified_organization.name

    # Clear database after tests
    truncate_db_tables()


def test_organization_modify_by_id_non_existent(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/organization/org-some-random-public-key-onlin",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Organization with the given ID does not exists"
    )

    # Clear database after tests
    truncate_db_tables()


def test_organization_modify_by_id_not_authorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    administrator = administrator_login(client, seed)
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

    # Clear database after tests
    truncate_db_tables()


def test_organization_delete_by_id_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/organization/{organization.id}",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    deleted_organization = Organization.find_by_id(organization.id)

    assert response.status_code == 200
    assert (
        response.json["message"]
        == f"Organization <{organization.id}> deleted successfully."
    )
    assert deleted_organization == None

    # Clear database after tests
    truncate_db_tables()


def test_organization_delete_by_id_non_existent(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/organization/org-some-random-public-key-onlin",
        json=organization_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Organization with the given ID does not exists"
    )

    # Clear database after tests
    truncate_db_tables()


def test_organization_delete_by_id_not_authorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/organization/{organization.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_organization_get_by_id_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/organization/{organization.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["administrator_id"]
    assert response.json["id"]
    assert response.json["name"]


def test_organization_get_by_id_not_authorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/organization/{organization.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_organization_get_by_id_not_found(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/organization/{organization.id[::-1]}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Organization with the given ID does not exists"
    )


def test_organization_get_administrator_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/organization/{organization.id}/administrator",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["email"]
    assert response.json["id"]
    assert response.json["name"]
    assert response.json["username"]


def test_organization_get_administrator_not_authorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/organization/{organization.id}/administrator",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )


def test_organization_get_administrator_not_found(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/organization/{organization.id[::-1]}/administrator",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Organization with the given ID does not exists"
    )

def test_organization_get_all_successful(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/organization/",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )
    
    assert response.status_code == 200
    assert response.json["organizations"]

def test_organization_get_all_unauthorized(client, seed):
    # Remove all data from database
    truncate_db_tables()

    # Initialize data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/organization/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )
    
    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )
