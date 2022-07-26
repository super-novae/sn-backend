from api.extensions import db
from secrets import token_hex


class Election(db.Model):
    __tablename__ = "sn_election"

    id = db.Column(db.String(length=32), nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(length=120), nullable=False, unique=True)
    route_name = db.Column(db.String(length=50), nullable=False, unique=True)
    organization_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_organization.id")
    )

    def __init__(self, name, organization_id, route_name):
        self.id = f"elec-{token_hex()[:27]}"
        self.name = name
        self.route_name = route_name
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


class Office(db.Model):
    __tablename__ = "sn_office"
    
    id = db.Column(db.String(length=32), nullable=False, primary_key=True)
    name = db.Column(db.String(length=60), nullable=False)
    route_name = db.Column(db.String(length=50), nullable=False)
    election_id = db.Column(db.String(length=32), db.ForeignKey("sn_election.id"))
    
    def __init__(self, name, route_name, election_id) -> None:
        self.id = f"off-{token_hex()[:28]}"
        self.name = name
        self.route_name = route_name
        self.election_id = election_id
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_all_by_election_id(cls, election_id):
        return cls.query.filter_by(election_id=election_id)


class Candidate(db.Model):
    __tablename__ = "sn_candidate"

    id = db.Column(db.String(length=32), nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(length=80), nullable=False, unique=True)
    profile_image_url = db.Column(db.String(length=150), default="cand-default.jpg")
    programme = db.Column(db.String(length=100), nullable=False)
    organization_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_organization.id")
    )
    election_id = db.Column(db.String(length=32), db.ForeignKey("sn_election.id"))
    office_id = db.Column(db.String(length=32), db.ForeignKey("sn_office.id"))

    def __init__(self, name, organization_id, programme, election_id, office_id):
        self.id = f"cand-{token_hex()[:27]}"
        self.name = name
        self.profile_image_url = f"https://url-to-s3-buckets/candidates/{self.id}"
        self.programme = programme
        self.organization_id = organization_id
        self.election_id = election_id
        self.office_id = office_id

    @classmethod
    def find_candidate_by_id(cls, id, election_id):
        return cls.query.filter_by(id=id, election_id=election_id).first()

    @classmethod
    def find_all_candidates_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id).all()

    @classmethod
    def find_all_candidates_by_election_id(cls, election_id):
        return cls.query.filter_by(election_id=election_id).all()
    
