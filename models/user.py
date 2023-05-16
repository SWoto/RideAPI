from passlib.hash import pbkdf2_sha256

from db import db
from models import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.String(32), db.ForeignKey(
        "roles.id"), unique=False, nullable=False)

    role = db.relationship("UserRoleModel")
    vehicles = db.relationship(
        "VehicleModel", back_populates="user", lazy="dynamic")

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self.password = pbkdf2_sha256.hash(kwargs["password"])

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
