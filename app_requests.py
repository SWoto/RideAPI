import os

from db import db
from app import create_app


API_NAME = "Rides MS."


if __name__ == "__main__":
    app = create_app(API_NAME, blueprints=[])

    if app.config['DEBUG']:
        with app.app_context():
            @app.before_first_request
            def create_tables():
                db.create_all()

    app.run(host="0.0.0.0", port=os.getenv("REQUESTS_API_PORT"))