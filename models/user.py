from passlib.hash import pbkdf2_sha256

from database.db import db
from models import BaseModel, UserRoleModel


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
    #rides_passanger = db.relationship("RideModel", foreign_keys="RideModel.passanger_id", viewonly=True)
    #rides_driver = db.relationship("RideModel", foreign_keys="RideModel.driver_id", viewonly=True)
    


    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self.password = pbkdf2_sha256.hash(kwargs["password"])

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def __find_role_type_by_id(cls, _id, role_type):
        return cls.query.join(cls.role).filter(UserRoleModel.name==role_type, cls.id==_id).first()
    
    @classmethod
    def find_driver_by_id(cls, _id):
        return cls.__find_role_type_by_id(_id, "driver")
    
    @classmethod
    def find_passanger_by_id(cls, _id):
        return cls.__find_role_type_by_id(_id, "passanger")