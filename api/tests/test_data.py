from .setup import truncate_db_tables
from ..test_data.superuser_data import superuser_create
from ..test_data.admin_data import administrator_signup
from ..test_data.organization_data import organization_create
from ..test_data.election_data import (
    election_create,
    office_create,
    candidate_create,
)
from ..test_data.voter_data import (
    voter_create,
    voter_login,
    voter_create_vote,
)
from random import randint


def test_data_get_election_results(client):
    # Clear database before tests
    truncate_db_tables()

    # Create seed to generate the same data
    seed = randint(1, 200)

    # Initialize the data and model instances
    superuser_create()
    administrator_signup(client)
    organization = organization_create()
    election = election_create()
    office_create()
    candidate_create()
    voter_create(seed)
    voter_create_vote(seed)

    voter = voter_login(client, seed)

    response = client.get(
        f"/api/v1/data/?organization_id={organization.id}&election_id={election.id}",
        headers={"Authorization": f"Bearer {voter['auth_token']}"},
    )

    assert response.status_code == 200
    assert response.json["results"]

    # Clear database after tests
    truncate_db_tables()
