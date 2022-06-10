from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from faker import Faker

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
fake = Faker()
