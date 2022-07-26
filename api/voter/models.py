from datetime import datetime
from api.extensions import db, bcrypt
from os import environ
from dotenv import load_dotenv
from secrets import token_urlsafe

# Load environment variables
load_dotenv()

class Voter(db.Model):
    __tablename__ = "sn_voter"

    id = db.Column(db.String(length=32), nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), nullable=False)
    password_hash = db.Column(db.String(length=130), nullable=False)
    telephone_number = db.Column(db.String(10), nullable=False, unique=True)
    organization_id = db.Column(db.String(length=32), db.ForeignKey("sn_organization.id", nullable=False))
    
    def __init__(self, name, username, email, telephone_number, organization_id):
        self.id = f"voter-{token_urlsafe()[:26]}"
        self.name = name
        self.username = username
        self.email = email
        self.telephone_number = telephone_number
        self.organization_id = organization_id
    
    @property
    def password():
        return "Password can only be set"
    
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
    def find_all_by_voter_group_id(cls):
        return cls.query.all()
    

class VoterGroup(db.Model):
    __tablename__ = "sn_voter_group"

    id = db.Column(db.String(length=32), nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    organization_id = db.Column(db.String(length=32), db.ForeignKey("sn_organization.id", nullable=False))
    
    def __init__(self, name, organization_id):
        self.id = f"voter-{token_urlsafe()[:26]}"
        self.name = name
        self.organization_id = organization_id
    
    @classmethod
    def find_all_voter_groups_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id)

class VoterGroupVoter(db.Model):
    __tablename__ = "sn_voter_group_voter"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voter_id = db.Column(db.String(length=32), db.ForeignKey("sn_voter.id"), nullable=False)
    voter_group_id = db.Column(db.String(length=32), db.ForeignKey("sn_voter_group.id"), nullable=False)

class VoterGroupElection(db.Model):
    __tablename__ = "sn_voter_group_election"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voter_group_id = db.Column()
    election_id = db.Column()

class Votes(db.Model):
    __tablename__ = "sn_voter"
    voter_id = db.Column(db.String(length=32), db.ForeignKey("sn_voter.id"), nullable=False)
    election_id = db.Column(db.String(length=32), db.ForeignKey("sn_election.id"), nullable=False)
    candidate_id = db.Column(db.String(length=32), db.ForeignKey("sn_candidate.id"), nullable=False)
    office_id = db.Column(db.String(length=32), db.ForeignKey("sn_office.id"), nullable=False)