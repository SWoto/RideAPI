from db import db

#TODO: Add test
class VehicleModel(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.String(32), primary_key=True)
    manufacturer = db.Column(db.String(254), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    license_plate = db.Column(db.String(7), unique=True, nullable=False)
    consumption = db.Column(db.Numeric(precision=4, scale=2), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey(
        "users.id"), unique=False, nullable=False)
    
    user = db.relationship("UserModel", back_populates="vehicles")

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
