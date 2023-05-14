import os

from db import db
from app import create_app
from resources.user import blp as UserBlueprint


API_NAME = "Users MS."
BLUEPRINTS = [UserBlueprint]


if __name__ == "__main__":
    app = create_app(API_NAME, blueprints=BLUEPRINTS)

    if app.config['DEBUG']:
        with app.app_context():
            @app.before_first_request
            def create_tables():
                db.create_all()

    app.run(host="0.0.0.0", port=os.getenv("USERS_API_PORT"))
