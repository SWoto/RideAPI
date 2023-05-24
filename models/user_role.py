from db import db
from models import BaseModel


class UserRoleModel(BaseModel):
    __tablename__ = "roles"
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __init__(self, **kwargs):
        super(UserRoleModel, self).__init__(**kwargs)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
