from db import db
from models import BaseModel


class VehicleModel(BaseModel):
    __tablename__ = "vehicles"

    manufacturer = db.Column(db.String(254), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    license_plate = db.Column(db.String(7), unique=True, nullable=False)
    consumption = db.Column(db.Numeric(precision=4, scale=2), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey(
        "users.id"), unique=False, nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("UserModel", back_populates="vehicles")

    def __init__(self, **kwargs):
        super(VehicleModel, self).__init__(**kwargs)

    @classmethod
    def find_by_license_plate(cls, plate):
        return cls.query.filter_by(license_plate=plate).first()

    @classmethod
    def get_user_active_vehicles(cls, _user_id):
        return cls.query.filter_by(user_id = _user_id, active=True).all()

    def deactiate(self):
        self.active = False
        db.session.commit()

    def activete(self):
        self.active = True
        db.session.commit()
