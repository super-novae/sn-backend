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
    candidate_get_test_instance,
)


def test_election_create_successful(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    administrator = administrator_login(client)

    response = client.post(
        "/api/v1/elections/",
        json=election_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 201
    assert response.json["name"] == election_details()["name"]
    assert response.json["organization_id"] == election_details()["organization_id"]

    # Clear database after tests
    truncate_db_tables()


def test_election_create_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
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


def test_election_modify_successful(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.put(
        f"/api/v1/elections/{election_test_instance.id}",
        json=election_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    modified_election = Election.find_by_id(
        election_test_instance.id
    )
    assert response.status_code == 200
    assert response.json["message"] == "Election modified successfully"
    assert modified_election.name == election_modified_details()["name"]

    # Clear database after tests
    truncate_db_tables()


def test_election_modify_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
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


def test_election_modify_non_existent(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.put(
        f"/api/v1/elections/elec-{election_test_instance.id[5:][::-1]}",
        json=election_modified_details(),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "An election with the given ID does not exist"

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_successful(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.delete(
        f"/api/v1/elections/{election_test_instance.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    deleted_election = Election.find_by_id(
        election_test_instance.id
    )

    assert response.status_code == 200
    assert response.json["message"] == "Election deleted successfully"
    assert deleted_election == None

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
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


def test_election_delete_non_existent(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.delete(
        f"/api/v1/elections/elec-{election_test_instance.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "An election with the given ID does not exist"

    # Clear database after tests
    truncate_db_tables()


def test_election_get_by_id_successful(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.get(
        f"/api/v1/elections/{election_test_instance.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["name"] == election_get_test_instance().name
    assert (
        response.json["organization_id"] == election_get_test_instance().organization_id
    )

    # Clear database after tests
    truncate_db_tables()


def test_election_get_by_id_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
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


def test_election_get_by_id_non_existent(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    election_test_instance = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.get(
        f"/api/v1/elections/elec-{election_test_instance.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "An election with the given ID does not exist"

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_by_organization_id_successful(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    organization = organization_get_test_instance()
    administrator = administrator_login(client)

    response = client.get(
        f"/api/v1/elections/organization/{organization.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["elections"]

    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_by_organization_id_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
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


def test_election_create_candidate_successful(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()

    organization = organization_get_test_instance()
    election = election_get_test_instance()
    administrator = administrator_login(client)

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


def test_election_create_candidate_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()

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


def test_election_modify_candidate_successful(client):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    candidate = candidate_create()

    election = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.put(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
        json=candidate_modified_details(),
    )
    
    assert response.status_code == 200
    assert response.json['message'] == "Candidate modified successfully"

    # Clear database after tests
    truncate_db_tables()


def test_election_modify_candidate_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
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


def test_election_modify_candidate_non_existent(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election_create()
    candidate = candidate_create()

    election = election_get_test_instance()
    administrator = administrator_login(client)

    response = client.put(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id[:5] + candidate.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
        json=candidate_modified_details(),
    )
    
    assert response.status_code == 404
    assert response.json['message'] == "A candidate with the given ID does not exist"

    # Clear database after tests
    truncate_db_tables()


def test_election_delete_candidate_successful(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election = election_create()
    candidate = candidate_create()
    
    administrator = administrator_login(client)

    
    response = client.delete(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )
    
    assert response.status_code == 200
    assert response.json['message'] == "Candidate deleted successfully"


    # Clear database after tests
    truncate_db_tables()


def test_election_delete_candidate_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election = election_create()
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


def test_election_delete_candidate_non_existent(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election = election_create()
    candidate = candidate_create()
    
    administrator = administrator_login(client)

    response = client.delete(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id[:5] + candidate.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )
    
    assert response.status_code == 404
    assert response.json['message'] == "A candidate with the given ID does not exist"

    # Clear database after tests
    truncate_db_tables()


def test_election_get_candidate_by_id_successful(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization = organization_create()
    election = election_create()
    candidate = candidate_create()
    
    administrator = administrator_login(client)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json['name'] == candidate.name
    assert response.json['election_id'] == election.id
    assert response.json['organization_id'] == organization.id

    # Clear database after tests
    truncate_db_tables()


def test_election_get_candidate_by_id_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization = organization_create()
    election = election_create()
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


def test_election_get_candidate_by_id_non_existent(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization = organization_create()
    election = election_create()
    candidate = candidate_create()
    
    administrator = administrator_login(client)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/{candidate.id[:5] + candidate.id[5:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )
    
    assert response.status_code == 404
    assert response.json['message'] == "A candidate with the given ID does not exist"    
    
    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_candidates_by_election_id_successful(client):
    # Clear database before tests
    truncate_db_tables()
    
    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization_create()
    election = election_create()
    candidate_create()
    
    administrator = administrator_login(client)

    response = client.get(
        f"/api/v1/elections/{election.id}/candidates/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )
    
    assert response.status_code == 200
    assert response.json['candidates']
    
    
    # Clear database after tests
    truncate_db_tables()


def test_election_get_all_candidates_by_election_id_unauthorized(client):
    # Clear database before tests
    truncate_db_tables()
    
        # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization = organization_create()
    election = election_create()
    candidate = candidate_create()
    
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
