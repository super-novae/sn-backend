from apiflask import APIFlask
from .extensions import *
from .config import config_dict
from dotenv import load_dotenv
from os import getenv
from .superuser.controllers import superuser
from .administrator.controllers import administrator
from .organization.controllers import organization
from .election.controllers import election
from .voter.controllers import voters

# Load environment variables
load_dotenv()


def create_app():
    app = APIFlask(__name__, title="sn-backend", version="1.0.0", docs_ui="redoc")

    # Load configurations
    app.config.from_object(config_dict[getenv("FLASK_ENV")])

    # Load extensions
    cors.init_app(app=app)
    db.init_app(app=app)
    bcrypt.init_app(app=app)
    jwt.init_app(app=app)
    migrate.init_app(app=app, db=db, compare_type=True)

    # Register blueprints for the application
    app.register_blueprint(superuser)
    app.register_blueprint(administrator)
    app.register_blueprint(organization)
    app.register_blueprint(election)
    app.register_blueprint(voters)

    return app
