import uuid

from db import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(32), primary_key=True)
    # TODO: Maybe add created and updated later...
    # created_on = db.Column(db.DateTime, default=db.func.now())
    # updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        self.id = uuid.uuid4().hex

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
