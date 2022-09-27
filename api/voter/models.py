from datetime import datetime
from api.extensions import db, bcrypt
from os import environ
from dotenv import load_dotenv
from secrets import token_urlsafe

# Load environment variables
load_dotenv()


class Voter(db.Model):
    __tablename__ = "sn_voter"

    id = db.Column(
        db.String(length=32), nullable=False, unique=True, primary_key=True
    )
    student_id = db.Column(db.String(length=8), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    telephone_number = db.Column(db.String(10), nullable=False, unique=True)
    college = db.Column(db.String(length=100), nullable=False)
    programme = db.Column(db.String(length=100), nullable=False)
    year = db.Column(db.String(length=6), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)
    password_hash = db.Column(db.String(length=130), nullable=False)
    organization_id = db.Column(
        db.String(length=32),
        db.ForeignKey("sn_organization.id"),
        nullable=False,
    )

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        telephone_number: str,
        college: str,
        programme: str,
        year: str,
        organization_id: str,
        password: str = None,
    ):
        self.id = f"voter-{token_urlsafe()[:26]}"
        self.student_id = student_id
        self.name = name
        self.email = email
        self.telephone_number = telephone_number
        self.college = college
        self.programme = programme
        self.year = year
        self.organization_id = organization_id
        self.date_created = datetime.today()

        splitted_name: str = name.lower().split(" ")

        if len(splitted_name) > 1:
            self.username = (
                splitted_name[1][0]
                + splitted_name[0][:9]
                + "-"
                + token_urlsafe()[:4]
            )
        else:
            self.username = (
                splitted_name[1][0]
                + splitted_name[0][:9]
                + "-"
                + token_urlsafe()[:4]
            )

    @property
    def password():
        return "Password can only be set"

    @password.setter
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
    def find_by_id_and_organization_id(cls, id, organization_id):
        return cls.query.filter_by(
            id=id, organization_id=organization_id
        ).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id).all()


class Vote(db.Model):
    __tablename__ = "sn_vote"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voter_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_voter.id"), nullable=False
    )
    election_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_election.id"), nullable=False
    )
    candidate_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_candidate.id"), nullable=False
    )
    office_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_office.id"), nullable=False
    )

    # TODO: Check if voter has already using the voter id & office id
    @classmethod
    def voter_vote_exists(cls, voter_id, office_id):
        return cls.query.filter_by(
            voter_id=voter_id, office_id=office_id
        ).first()

    # TODO: Retrive all src votes (results)
    # @classmethod
    # def votes_get_src_results(cls):
    #     return

    # TODO: Retrive college level vote (results)
    # TODO: Retrieve all voter votes (results)
