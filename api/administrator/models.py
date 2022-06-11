from api.extensions import db
import secrets


class Administrator(db.Model):
    __tablename__ = "sn_administrator"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), nullable=False)
    password_hash = db.Column(db.String(130), nullable=False)

    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email
        self.public_id = secrets.token_hex(64)

    @property
    def password():
        return "Password can only be set"

    @property().setter
    def password(self, password):
        self.password_hash = ""

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
