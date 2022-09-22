from api.extensions import db
from secrets import token_hex


class Organization(db.Model):
    __tablename__ = "sn_organization"

    id = db.Column(
        db.String(length=32), nullable=False, unique=True, primary_key=True
    )
    name = db.Column(db.String(length=256), nullable=False)
    elections = db.relationship("Election")
    administrator_id = db.Column(
        db.String(length=32),
        db.ForeignKey("sn_administrator.id"),
        nullable=True,
    )

    def __init__(self, name):
        self.id = f"org-{token_hex()[:28]}"
        self.name = name

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_administrator_id(cls, admin_id):
        return cls.query.filter_by(administrator_id=admin_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
