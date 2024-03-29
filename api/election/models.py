from api.extensions import db
from secrets import token_hex


class Election(db.Model):
    __tablename__ = "sn_election"

    id = db.Column(
        db.String(length=32), nullable=False, unique=True, primary_key=True
    )
    name = db.Column(db.String(length=120), nullable=False, unique=True)
    state = db.Column(db.String(length=10), nullable=False, default="on-hold")
    route_name = db.Column(db.String(length=50), nullable=True)
    type = db.Column(db.String(length=10), nullable=False)
    college = db.Column(db.String(length=100), nullable=True)
    programme = db.Column(db.String(length=100), nullable=True)
    organization_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_organization.id")
    )
    candidates = db.relationship(
        "Candidate", backref="election", lazy="joined", cascade="all, delete"
    )
    offices = db.relationship(
        "Office", backref="election", lazy="joined", cascade="all, delete"
    )

    def __init__(
        self, name, route_name, type, organization_id, college="", programme=""
    ):
        self.id = f"elec-{token_hex()[:27]}"
        self.name = name
        self.route_name = route_name
        self.type = type
        self.college = college
        self.programme = programme
        self.organization_id = organization_id

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_type(cls, type, organization_id):
        return cls.query.filter_by(
            type=type, organization_id=organization_id
        ).all()

    @classmethod
    def find_by_college(cls, college, organization_id):
        return cls.query.filter_by(
            college=college, type="College", organization_id=organization_id
        ).all()

    @classmethod
    def find_by_programme(cls, programme, organiztion_id):
        return cls.query.filter_by(
            programme=programme,
            type="Department",
            organization_id=organiztion_id,
        ).all()

    @classmethod
    def find_by_id_and_organization_id(cls, id, organization_id):
        return cls.query.filter_by(
            id=id, organization_id=organization_id
        ).first()

    @classmethod
    def find_all_elections_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organization_id=organization_id).all()


class Office(db.Model):
    __tablename__ = "sn_office"

    id = db.Column(db.String(length=32), nullable=False, primary_key=True)
    name = db.Column(db.String(length=60), nullable=False)
    route_name = db.Column(db.String(length=50), nullable=False)
    election_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_election.id")
    )
    candidates = db.relationship(
        "Candidate", backref="office", lazy="joined", cascade="all, delete"
    )

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
        return cls.query.filter_by(election_id=election_id).all()


class Candidate(db.Model):
    __tablename__ = "sn_candidate"

    id = db.Column(
        db.String(length=32), nullable=False, unique=True, primary_key=True
    )
    name = db.Column(db.String(length=80), nullable=False, unique=True)
    profile_image_url = db.Column(
        db.String(length=150), default="cand-default.jpg"
    )
    programme = db.Column(db.String(length=100), nullable=False)
    organization_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_organization.id")
    )
    election_id = db.Column(
        db.String(length=32), db.ForeignKey("sn_election.id")
    )
    office_id = db.Column(db.String(length=32), db.ForeignKey("sn_office.id"))
    votes = db.relationship(
        "Vote", backref="candidate", lazy="joined", cascade="all, delete"
    )

    def __init__(
        self, name, organization_id, programme, election_id, office_id
    ):
        self.id = f"cand-{token_hex()[:27]}"
        self.name = name
        self.profile_image_url = (
            f"https://url-to-s3-buckets/candidates/{self.id}"
        )
        self.programme = programme
        self.organization_id = organization_id
        self.election_id = election_id
        self.office_id = office_id

    @classmethod
    def find_candidate_by_id(cls, id, election_id):
        return cls.query.filter_by(id=id, election_id=election_id).first()

    # @classmethod
    # def find_all_candidates_by_organization_id(cls, organization_id):
    #     return cls.query.filter_by(organization_id=organization_id).all()

    @classmethod
    def find_all_candidates_by_election_id(cls, election_id):
        return cls.query.filter_by(election_id=election_id).all()

    @classmethod
    def find_all_candidates_by_office_id(cls, office_id):
        return cls.query.filter_by(office_id=office_id).all()
