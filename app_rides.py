import os


from db import db
from base_app import create_app
from resources.ride import blp as RideBlueprint


API_NAME = "Rides MS."
BLUEPRINTS = [RideBlueprint]


if __name__ == "__main__":
    app = create_app(API_NAME, blueprints=BLUEPRINTS)

    if app.config['DEBUG']:
        with app.app_context():
            @app.before_first_request
            def create_tables():
                db.create_all()

    app.run(host="0.0.0.0", port=os.getenv("RIDES_API_PORT"))
