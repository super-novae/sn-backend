from api.extensions import db
from secrets import token_hex


class Organization(db.Model):
    __tablename__ = "sn_organization"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(length=32), nullable=False, unique=True)
    name = db.Column(db.String(length=256), nullable=False)
    elections = db.relationship("Election")
    administrator_id = db.Column(db.Integer, db.ForeignKey("sn_administrator.id"), nullable=False)

    def __init__(self, name, administrator_id):
        self.public_id = f"org-{token_hex()[:28]}"
        self.name = name
        self.administrator_id = administrator_id

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
