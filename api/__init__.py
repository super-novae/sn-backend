from apiflask import APIFlask
from .extensions import *
from dotenv import load_dotenv
from .administrator.controllers import administrator

# Load environment variables
load_dotenv()


def create_app():
    app = APIFlask(__name__, title="sn-backend", version="1.0.0")

    # Load extensions
    cors.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # Register blueprints for the application
    app.register_blueprint(administrator)

    return app
