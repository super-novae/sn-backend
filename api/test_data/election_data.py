from api.extensions import fake, db
from ..election.models import Election, Office, Candidate
from .organization_data import organization_get_test_instance


def election_details():
    organization = organization_get_test_instance()
    return {
        "name": organization.name + " Elections",
        "organization_id": organization.id,
        "route_name": fake.word()
    }


def election_modified_details():
    organization = organization_get_test_instance()
    return {"name": organization.name + " Modified Elections"}


def election_create() -> Election:
    data = election_details()
    election = Election(**data)

    db.session.add(election)
    db.session.commit()

    return election


def election_get_test_instance() -> Election:
    return Election.query.filter_by(name=election_details()["name"]).first()

def office_details():
    election = election_get_test_instance()
    return {"name": "President", "route_name": "gadres", "election_id": election.id}

def office_modified_details():
    return {"name": "Vice President", "route_name": "aces"}

def office_create() -> Office:
    data = office_details()
    office = Office(**data)
    
    db.session.add(office)
    db.session.commit()

    return office

def office_get_test_instance() -> Office:
    return Office.query.filter_by(name=office_details()["name"], route_name=office_details()["route_name"]).first()

def candidate_details():
    organization = organization_get_test_instance()
    election = election_get_test_instance()
    office = office_get_test_instance()
    
    return {
        "name": fake.name(),
        "organization_id": organization.id,
        "election_id": election.id,
        "office_id": office.id,
        "programme": "Bsc. Computer Engineering"
    }


def candidate_modified_details():
    return {"name": fake.name()}


def candidate_create() -> Candidate:
    data = candidate_details()
    candidate = Candidate(**data)

    db.session.add(candidate)
    db.session.commit()

    return candidate


def candidate_get_test_instance(id) -> Candidate:
    return Candidate.find_candidate_by_id(id)
