from api.extensions import db
from secrets import token_hex


class Election(db.Model):
    __tablename__ = "sn_election"

    id = db.Column(db.String(length=32), nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(length=120), nullable=False, unique=True)
    organization_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_organization.id")
    )

    def __init__(self, name, organization_id):
        self.id = f"elec-{token_hex()[:27]}"
        self.name = name
        self.organization_id = organization_id

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all_elections_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id).all()

    # @classmethod
    # def find_all_elections_by_voter_id(cls, voter_id):
    #     return cls.query.filter_by(voter_id=voter_id).all()


class Candidate(db.Model):
    __tablename__ = "sn_candidate"

    id = db.Column(db.String(length=32), nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(length=80), nullable=False, unique=True)
    profile_image_url = db.Column(db.String(length=150), default="cand-default.jpg")
    organization_id = db.Column(db.String(length=32), db.ForeignKey("sn_organization.id"))
    election_id = db.Column(db.String(length=32), db.ForeignKey("sn_election.id"))

    def __init__(self, name, organization_id, election_id):
        self.id = f"cand-{token_hex()[:27]}"
        self.name = name
        self.profile_image_url = f"https://url-to-s3-buckets/candidates/{self.id}"
        self.organization_id = organization_id
        self.election_id = election_id

    @classmethod
    def find_candidate_by_id(cls, id, election_id):
        return cls.query.filter_by(id=id, election_id=election_id).first()

    @classmethod
    def find_all_candidates_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id).all()

    @classmethod
    def find_all_candidates_by_election_id(cls, election_id):
        return cls.query.filter_by(election_id=election_id).all()
