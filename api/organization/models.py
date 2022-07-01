from api.extensions import db
from secrets import token_hex

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(length=32), nullable=False, unique=True)
    name = db.Column(db.String(length= 256), nullable=False)
    
    def __init__(self, name):
        self.public_id = f"org-{token_hex()[:28]}"
        self.name = name
    
    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()