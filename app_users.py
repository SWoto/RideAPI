import os

from database.db import db
from base_app import create_app
from resources.user import blp as UserBlueprint
from models import UserRoleModel

API_NAME = "Users MS."
BLUEPRINTS = [UserBlueprint]


if __name__ == "__main__":
    app = create_app(API_NAME, blueprints=BLUEPRINTS)

    with app.app_context():
        role_passanger = {"name": "passanger"}
        role_admin = {"name": "driver"}
        if not UserRoleModel.find_by_name(**role_passanger):
            db.session.add(UserRoleModel(**role_passanger))
        if not UserRoleModel.find_by_name(**role_admin):
            db.session.add(UserRoleModel(**role_admin))
        db.session.commit()

    app.run(host="0.0.0.0", port=os.getenv("USERS_API_PORT"))
