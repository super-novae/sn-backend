from .setup import truncate_db_tables
from ..election.models import Election
from ..test_data.superuser_data import superuser_create, superuser_login
from ..test_data.admin_data import administrator_signup, administrator_login
from ..test_data.organization_data import (
    organization_create,
    organization_get_test_instance,
)
from ..test_data.election_data import (
    election_create,
    election_details,
    election_modified_details,
    election_get_test_instance,
    candidate_create,
    candidate_details,
    candidate_modified_details,
    office_create,
    office_details,
    office_modified_details,
)
from ..test_data.voter_data import voter_create, voter_login
from random import randint


def test_election_create_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    administrator = administrator_login(client, seed)

    response = client.post(
        "/api/v1/elections/",
        json=election_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 201
    assert response.json["name"] == election_details()["name"]
    assert (
        response.json["organization_id"]
        == election_details()["organization_id"]
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_create_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    superuser = superuser_login(client)

    response = client.post(
        "/api/v1/elections/",
        json=election_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_modify_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.put(
        f"/api/v1/elections/{election_test_instance.id}",
        json=election_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    modified_election = Election.find_by_id(election_test_instance.id)
    assert response.status_code == 200
    assert response.json["message"] == "Election modified successfully"
    assert modified_election.name == election_modified_details()["name"]

    # Clear database after tests
    truncate_db_tables()


def test_election_modify_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/elections/{election_test_instance.id}",
        json=election_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_modify_non_existent(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.put(
        f"/api/v1/elections/elec-{election_test_instance.id[5:][::-1]}",
        json=election_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An election with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/elections/{election_test_instance.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    deleted_election = Election.find_by_id(election_test_instance.id)

    assert response.status_code == 200
    assert response.json["message"] == "Election deleted successfully"
    assert deleted_election == None

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/elections/{election_test_instance.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_non_existent(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/elections/elec-{election_test_instance.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An election with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_by_id_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/{election_test_instance.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["name"] == election_get_test_instance().name
    assert (
        response.json["organization_id"]
        == election_get_test_instance().organization_id
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_by_id_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/elections/{election_test_instance.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_by_id_non_existent(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/elec-{election_test_instance.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An election with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_by_id_full_details_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()
    voter_create(seed)

    voter = voter_login(client, seed)

    response = client.get(
        f"api/v1/elections/{election.id}/full_details",
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["election"]
    assert response.json["offices"]

    # Clear database before tests
    truncate_db_tables()


def test_election_get_by_id_full_details_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()
    voter_create(seed)

    superuser = superuser_login(client)

    response = client.get(
        f"api/v1/elections/{election.id}/full_details",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_by_id_full_details_does_not_exist(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()
    voter_create(seed)

    voter = voter_login(client, seed)

    response = client.get(
        f"api/v1/elections/elec-{election.id[5:][::-1]}/full_details",
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An election with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_by_organization_id_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    organization = organization_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/organization/{organization.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["elections"]

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_by_organization_id_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    organization = organization_get_test_instance()
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/elections/organization/{organization.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_office_create_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()

    administrator = administrator_login(client, seed)

    response = client.post(
        f"/api/v1/elections/{election.id}/office/",
        json=office_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 201
    assert response.json["election_id"] == election.id
    assert len(response.json) == 4

    # Clear database after tests
    truncate_db_tables()


def test_create_office_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()

    superuser = superuser_login(client)

    response = client.post(
        f"/api/v1/elections/{election.id}/office/",
        json=office_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_modify_office_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    administrator = administrator_login(client, seed)

    response = client.put(
        f"/api/v1/elections/{election.id}/office/{office.id}",
        json=office_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Office modified successfully"
    assert office.route_name == office_modified_details()["route_name"]

    # Clear database after tests
    truncate_db_tables()


def test_modify_office_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    superuser = superuser_login(client)

    response = client.put(
        f"/api/v1/elections/{election.id}/office/{office.id}",
        json=office_modified_details(),
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_modify_office_not_found(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    administrator = administrator_login(client, seed)

    response = client.put(
        f"/api/v1/elections/{election.id}/office/{office.id[:4] + office.id[4:][::-1]}",
        json=office_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An office with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_delete_office_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/elections/{election.id}/office/{office.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Office deleted successfully"

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_office_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/elections/{election.id}/office/{office.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_office_not_found(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/elections/{election.id}/office/{office.id[:4] + office.id[4:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An office with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_office_by_id_succesful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/{election.id}/office/{office.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["election_id"] == election.id
    assert response.json["id"]

    # Clear database after tests
    truncate_db_tables()


def test_election_get_office_by_id_office_not_found(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/{election.id}/office/{office.id[:4] + office.id[4:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An office with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_office_by_id_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office = office_create()

    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/elections/{election.id}/office/{office.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_offices_by_election_id_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()

    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/{election.id}/office/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["offices"]
    assert response.json["offices"][0]["id"]
    assert response.json["offices"][0]["election_id"] == election.id

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_offices_by_election_id_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()

    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/elections/{election.id}/office/",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_create_candidate_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()

    organization = organization_get_test_instance()
    election = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.post(
        f"/api/v1/elections/{election.id}/candidates/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
        json=candidate_details(),
    )

    assert response.status_code == 201
    assert response.json["election_id"] == election.id
    assert response.json["organization_id"] == organization.id

    # Clear database after tests
    truncate_db_tables()


def test_election_create_candidate_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()

    election = election_get_test_instance()
    superuser = superuser_login(client)

    response = client.post(
        f"/api/v1/elections/{election.id}/candidates/",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
        json=candidate_details(),
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_modify_candidate_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()
    candidate = candidate_create()

    election = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.put(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
        json=candidate_modified_details(),
    )

    assert response.status_code == 200
    assert response.json["message"] == "Candidate modified successfully"

    # Clear database after tests
    truncate_db_tables()


def test_election_modify_candidate_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()
    candidate = candidate_create()

    superuser = superuser_login(client)
    election = election_get_test_instance()

    response = client.put(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
        json=candidate_modified_details(),
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )
    # Clear database after tests
    truncate_db_tables()


def test_election_modify_candidate_non_existent(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()
    candidate = candidate_create()

    election = election_get_test_instance()
    administrator = administrator_login(client, seed)

    response = client.put(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id[:5] + candidate.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
        json=candidate_modified_details(),
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "A candidate with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_candidate_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate = candidate_create()

    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Candidate deleted successfully"

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_candidate_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate = candidate_create()

    superuser = superuser_login(client)

    response = client.delete(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_candidate_non_existent(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate = candidate_create()

    administrator = administrator_login(client, seed)

    response = client.delete(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id[:5] + candidate.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "A candidate with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_candidate_by_id_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    election = election_create()
    office_create()
    candidate = candidate_create()

    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["name"] == candidate.name
    assert response.json["election_id"] == election.id
    assert response.json["organization_id"] == organization.id

    # Clear database after tests
    truncate_db_tables()


def test_election_get_candidate_by_id_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate = candidate_create()

    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_candidate_by_id_non_existent(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate = candidate_create()

    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id[:5] + candidate.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "A candidate with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_candidates_by_election_id_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()

    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["candidates"]

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_candidates_by_election_id_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()

    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_change_state_success(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()

    administrator = administrator_login(client, seed)

    response = client.post(
        f"/api/v1/elections/{election.id}/change/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
        json={"state": "in-session"},
    )

    assert response.status_code == 200
    assert (
        response.json["message"]
        == f"Election {election.name} has been changed to {election.state}"
    )
    assert election.state == "in-session"

    # Clear database after tests
    truncate_db_tables()


def test_election_change_state_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()

    superuser = superuser_login(client)

    response = client.post(
        f"/api/v1/elections/{election.id}/change/",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
        json={"state": "in-session"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_change_state_election_not_found(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election = election_create()
    office_create()
    candidate_create()

    administrator = administrator_login(client, seed)

    response = client.post(
        f"/api/v1/elections/{election.id[:5] + election.id[5:][::-1]}/change/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
        json={"state": "in-session"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "An election with the given ID does not exist"
    )

    # Clear database after tests
    truncate_db_tables()
