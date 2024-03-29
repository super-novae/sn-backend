from flask import current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from faker import Faker
from werkzeug.local import LocalProxy

cors = CORS()
db = SQLAlchemy(session_options={"expire_on_commit": False})
mail = Mail()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
fake = Faker()
logger = LocalProxy(lambda: current_app.logger)
