import uuid
from passlib.hash import pbkdf2_sha256

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    vehicles = db.relationship("VehicleModel", back_populates="user", lazy="dynamic")

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self.id = uuid.uuid4().hex
        self.password = pbkdf2_sha256.hash(kwargs["password"])

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()