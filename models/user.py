import uuid

from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(32), primary_key=True, default=uuid.uuid4().hex)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, nullable=False)
