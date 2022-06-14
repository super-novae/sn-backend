from api.extensions import db


class Voter(db.Model):
    __tablename__ = "sn_voter"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    telephone_number = db.Column(db.String(10), nullable=False, unique=True)
    election_id = db.Column(db.Integer)


class VoterGroup(db.Model):
    __tablename__ = "sn_voter_group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
