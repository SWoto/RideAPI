from db import db
from models import BaseModel, UserModel


class RideModel(BaseModel):
    __tablename__ = "rides"

    distance = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
    gas_price = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
    passenger_id = db.Column(db.String(32), db.ForeignKey(
        "users.id"), unique=False, nullable=False)
    driver_id = db.Column(db.String(32), db.ForeignKey(
        "users.id"), unique=False, nullable=False)
    total_value = db.Column(db.Numeric(precision=5, scale=2), nullable=False)

    passenger = db.relationship("UserModel", foreign_keys=[passenger_id])
    driver = db.relationship("UserModel", foreign_keys=[driver_id])

    def __init__(self, **kwargs):
        super(RideModel, self).__init__(**kwargs)

    @classmethod
    def find_rides_passenger(cls, passenger_id):
        return cls.query.join(cls.user).filter(UserModel.id == passenger_id).all()

    @classmethod
    def find_rides_driver(cls, rider_id):
        return cls.query.join(cls.driver).filter(UserModel.id == rider_id).all()
