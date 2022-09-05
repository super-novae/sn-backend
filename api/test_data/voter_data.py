from api.extensions import fake, db
from api.voter.models import Voter, Vote
from api.generic.data import colleges, colleges_programmes, years
from api.test_data.election_data import (
    candidate_get_test_instance,
    election_get_test_instance,
    office_get_test_instance,
)
from api.test_data.organization_data import organization_get_test_instance
from random import randint, choice


def voter_details_single(seed=None):
    if seed:
        fake.seed_instance(seed)

    organization = organization_get_test_instance()
    selected_college = choice(colleges)
    voter = {
        "student_id": str(randint(20610000, 20820000)),
        "name": fake.name(),
        "email": fake.email(),
        "telephone_number": "0" + str(randint(540000000, 543000000)),
        "college": selected_college,
        "programme": choice(colleges_programmes[selected_college]),
        "year": choice(years[0:4]),
        "organization_id": organization.id,
        "password": fake.password(),
    }
    return voter


def voter_details_multiple():
    voters = []

    for _ in range(5):
        voter = voter_details_single()
        voter.pop("password")
        voters.append(voter)

    return voters


def voter_create(seed=None) -> Voter:
    data = voter_details_single(seed) if seed else voter_details_single()
    voter = Voter(**data)

    voter.password = data["password"]

    db.session.add(voter)
    db.session.commit()

    return voter


def voter_get_test_instance(seed) -> Voter:
    voter = voter_details_single(seed) if seed else voter_details_single(seed)
    return Voter.query.filter_by(
        name=voter["name"], email=voter["email"]
    ).first()


def voter_login_credentials(seed):
    if seed:
        fake.seed_instance(seed)
    voter = voter_details_single(seed) if seed else voter_details_single()
    return {"email": voter["email"], "password": voter["password"]}


def voter_login(client, seed):
    response = client.post(
        "/api/v1/voters/login", json=voter_login_credentials(seed)
    )

    return response.json


def voter_vote_details(seed):
    vote = {
        "voter_id": voter_get_test_instance(seed).id,
        "election_id": election_get_test_instance().id,
        "candidate_id": candidate_get_test_instance().id,
        "office_id": office_get_test_instance().id,
    }

    return vote


def voter_create_vote(seed):
    data = voter_vote_details(seed)

    vote = Vote(**data)

    db.session.add(vote)
    db.session.commit()

    return vote
