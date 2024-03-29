from api.test_data.admin_data import administrator_signup, administrator_login
from api.test_data.election_data import (
    candidate_create,
    election_create,
    office_create,
)
from api.test_data.organization_data import organization_create
from api.test_data.superuser_data import superuser_create, superuser_login
from api.test_data.voter_data import (
    voter_create_vote,
    voter_details_multiple,
    voter_details_single,
    voter_create,
    voter_login,
    voter_login_credentials,
    voter_vote_details,
)
from api.tests.setup import truncate_db_tables
from api.voter.models import Voter
from random import randint


def test_voter_signup_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()

    voter = voter_details_single()
    voter.pop("password")

    administrator = administrator_login(client, seed)

    response = client.post(
        "/api/v1/voters/signup",
        json=voter,
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    created_voter = Voter.find_by_email(voter["email"])

    assert response.status_code == 201
    assert response.json["email"] == created_voter.email
    assert response.json["id"] == created_voter.id

    # Clear database after tests
    truncate_db_tables()


def test_voter_signup_voter_already_exists(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    voter_create(seed)
    administrator = administrator_login(client, seed)

    voter_details = voter_details_single(seed)
    voter_details.pop("password")

    response = client.post(
        "/api/v1/voters/signup",
        json=voter_details,
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 409
    assert (
        response.json["message"]
        == "A voter with the given credentials already exists"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_signup_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()

    voter = voter_details_single()
    voter.pop("password")

    superuser = superuser_login(client)

    response = client.post(
        "/api/v1/voters/signup",
        json=voter,
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_bulk_signup_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    administrator = administrator_login(client, seed)

    voters = voter_details_multiple()

    response = client.post(
        "/api/v1/voters/signup-bulk",
        json={"voters": voters},
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    created_voters = Voter.query.all()

    assert response.status_code == 200
    assert response.json["message"] == "5 voters created successfully"
    assert len(created_voters) == 5

    # Clear database after tests
    truncate_db_tables()


def test_voter_bulk_signup_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    superuser = superuser_login(client)

    voters = voter_details_multiple()

    response = client.post(
        "/api/v1/voters/signup-bulk",
        json={"voters": voters},
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_bulk_signup_server_error(client, seed):
    pass  # TODO: Come back to this when i find a way to get 500


def test_voter_login_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    voter = voter_create(seed)

    response = client.post(
        "/api/v1/voters/login", json=voter_login_credentials(seed)
    )

    assert response.status_code == 200
    assert response.json["id"] == voter.id
    assert response.json["auth_token"]

    # Clear database after tests
    truncate_db_tables()


def test_voter_login_voter_does_not_exist(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    voter_create(seed)

    response = client.post(
        "/api/v1/voters/login", json=voter_login_credentials(seed + 1)
    )

    assert response.status_code == 400
    assert (
        response.json["message"]
        == "A voter with the given credentials does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_by_id_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    voter_create(seed)

    administrator = administrator_login(client, seed)
    voter = voter_login(client, seed)

    response = client.get(
        f"/api/v1/voters/{voter['id']}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    # TODO: Add some more assertions
    assert response.status_code == 200

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_by_id_voter_does_not_exist(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    voter_create(seed)

    administrator = administrator_login(client, seed)
    voter = voter_login(client, seed)

    response = client.get(
        f"/api/v1/voters/{voter['id'][:6] + voter['id'][6:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"] == "A voter with the given Id does not exist"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_by_id_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    voter_create(seed)

    voter = voter_login(client, seed)
    superuser = superuser_login(client)

    response = client.get(
        f"/api/v1/voters/{voter['id'][:6] + voter['id'][6:][::-1]}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_all_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    election_create()
    voter_create(seed)

    administrator = administrator_login(client, seed)
    voter_login(client, seed)

    response = client.get(
        f"/api/v1/voters/?organization_id={organization.id}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["voters"]
    assert len(response.json["voters"])

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_all_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    election_create()
    voter_create(seed)

    superuser = superuser_login(client)
    voter_login(client, seed)

    response = client.get(
        f"/api/v1/voters/?organization_id={organization.id}",
        headers={"Authorization": f"Bearer {superuser['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_all_organization_not_found(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    election_create()
    voter_create(seed)

    administrator = administrator_login(client, seed)
    voter_login(client, seed)

    response = client.get(
        f"/api/v1/voters/?organization_id={organization.id[:4] + organization.id[4:][::-1]}",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 404
    assert (
        response.json["message"]
        == "Organization with the given ID does not exists"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_all_organization_id_not_provided(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    voter_create(seed)

    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/voters/",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 400
    assert response.json["message"] == "Validation error"

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_elections_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    election_create()
    voter_create(seed)

    voter = voter_login(client, seed)

    response = client.get(
        f"/api/v1/voters/{voter['id']}/organization/{organization.id}/elections",
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["college_elections"] == []
    assert response.json["department_elections"] == []
    assert response.json["src_elections"]

    # Clear database after tests
    truncate_db_tables()


def test_voter_get_elections_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization = organization_create()
    election_create()
    voter_create(seed)

    voter = voter_login(client, seed)
    administrator = administrator_login(client, seed)

    response = client.get(
        f"/api/v1/voters/{voter['id']}/organization/{organization.id}/elections",
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_cast_vote_successful(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()
    candidate_create()
    voter_create(seed)

    voter = voter_login(client, seed)

    response = client.post(
        f"/api/v1/voters/{voter['id']}/vote",
        json=voter_vote_details(seed),
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 201
    assert response.json["id"]

    # Clear database after tests
    truncate_db_tables()


def test_voter_cast_vote_unauthorized(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()
    candidate_create()
    voter_create(seed)

    voter = voter_login(client, seed)
    administrator = administrator_login(client, seed)

    response = client.post(
        f"/api/v1/voters/{voter['id']}/vote",
        json=voter_vote_details(seed),
        headers={"Authorization": f"Bearer {administrator['auth_token']}"},
    )

    assert response.status_code == 403
    assert (
        response.json["message"]
        == "User does not have the required permissions to perform action"
    )

    # Clear database after tests
    truncate_db_tables()


def test_voter_cast_vote_voter_has_already_cast_vote(client, seed):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client, seed)
    organization_create()
    election_create()
    office_create()
    candidate_create()
    voter_create(seed)
    voter_create_vote(seed)

    voter = voter_login(client, seed)
    administrator_login(client, seed)

    response = client.post(
        f"/api/v1/voters/{voter['id']}/vote",
        json=voter_vote_details(seed),
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 400
    assert (
        response.json["message"]
        == "Voter has already voted for a candidate in this office"
    )

    # Clear database after tests
    truncate_db_tables()
