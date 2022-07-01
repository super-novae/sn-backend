from api.extensions import db, fake
from ..organization.models import Organization

data = {"name": fake.company()}


def organization_details():
    return data


def organization_modified_details():
    return {"name": fake.company()}


def organization_create():
    organization = Organization(**data)

    db.session.add(organization)
    db.session.commit()

    return organization
