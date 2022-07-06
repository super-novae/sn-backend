from api.extensions import db
from secrets import token_hex


class Election(db.Model):
    __tablename__ = "sn_election"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=120), nullable=False, unique=True)
    public_id = db.Column(db.String(length=32), nullable=False, unique=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("sn_organization.id"))

    def __init__(self, name, public_id, organization_id):
        self.name = name
        self.public_id = token_hex()[:32]
        self.organization_id = organization_id

    @classmethod
    def find_election_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    @classmethod
    def find_all_elections_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id).all()

    # @classmethod
    # def find_all_elections_by_voter_id(cls, voter_id):
    #     return cls.query.filter_by(voter_id=voter_id).all()


class Candidate(db.Model):
    __tablename__ = "sn_candidate"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=80), nullable=False, unique=True)
    public_id = db.Column(db.String(length=16), nullable=False, unique=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("sn_organization.id"))
    election_id = db.Column(db.Integer, db.ForeignKey("sn_election.id"))

    def __init__(self, organization_id, election_id):
        self.public_id = token_hex()[:16]
        self.organization_id = organization_id
        self.election_id = election_id

    @classmethod
    def find_candidate_by_public_id(cls, public_id, election_id):
        return cls.query.filter_by(public_id=public_id, election_id=election_id)

    @classmethod
    def find_all_candidates_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id).all()

    @classmethod
    def find_all_candidates_by_election_id(cls, election_id):
        return cls.query.filter_by(election_id=election_id).all()
