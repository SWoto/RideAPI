from db import db
from models import BaseModel


class RideModel(BaseModel):
    __tablename__ = "rides"
    
    distance = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), unique=False, nullable=False)
    driver_id = db.Column(db.String(32), db.ForeignKey("users.id"), unique=False, nullable=False)
    
    def __init__(self, **kwargs):
        super(RideModel, self).__init__(**kwargs)