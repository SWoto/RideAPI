import os

from db import db
from base_app import create_app
from resources.user import blp as UserBlueprint
from models import UserRoleModel

API_NAME = "Users MS."
BLUEPRINTS = [UserBlueprint]


if __name__ == "__main__":
    app = create_app(API_NAME, blueprints=BLUEPRINTS)

    if app.config['DEBUG']:
        with app.app_context():
            @app.before_first_request
            def create_tables():
                db.create_all()

            @app.before_first_request
            def fill_roles():
                role_user = {"name": "user"}
                role_admin = {"name": "driver"}
                if not UserRoleModel.find_by_name(**role_user):
                    db.session.add(UserRoleModel(**role_user))
                if not UserRoleModel.find_by_name(**role_admin):
                    db.session.add(UserRoleModel(**role_admin))
                db.session.commit()

    app.run(host="0.0.0.0", port=os.getenv("USERS_API_PORT"))
