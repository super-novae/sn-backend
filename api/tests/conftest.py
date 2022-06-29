import pytest
from api import create_app, db
from api.config import config_dict


@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.from_object(config_dict["test"])
    flask_app.app_context().push()
    yield flask_app


@pytest.fixture
def client(app):
    yield app.test_client()
