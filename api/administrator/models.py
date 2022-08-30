from datetime import datetime
from api.extensions import db, bcrypt
from os import environ
from dotenv import load_dotenv
from secrets import token_urlsafe

# Load environment variables
load_dotenv()


class Administrator(db.Model):
    __tablename__ = "sn_administrator"

    id = db.Column(
        db.String(length=32), nullable=False, unique=True, primary_key=True
    )
    name = db.Column(db.String(length=80), nullable=False)
    username = db.Column(db.String(length=15), nullable=False, unique=True)
    email = db.Column(db.String(length=80), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), nullable=False)
    password_hash = db.Column(db.String(length=130), nullable=False)

    def __init__(self, name, username, email, password=None):
        self.id = f"admin-{token_urlsafe()[:26]}"
        self.name = name
        self.username = username
        self.email = email
        self.date_created = datetime.today()

    # @property
    # def password():
    #     return "Password can only be set"

    @property().setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password, environ.get("BCRYPT_LOG_ROUNDS")
        ).decode(encoding="utf-8", errors="ignore")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
