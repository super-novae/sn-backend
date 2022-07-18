from api.extensions import db, fake
from ..organization.models import Organization
from ..test_data.admin_data import administrator_get_test_instance



def organization_details():
    admin = administrator_get_test_instance()
    return {"name": fake.company(), "administrator_id": admin.id}


def organization_modified_details():
    return {"name": fake.company()}


def organization_create() -> Organization:
    data = organization_details()
    organization = Organization(**data)

    db.session.add(organization)
    db.session.commit()

    return organization
