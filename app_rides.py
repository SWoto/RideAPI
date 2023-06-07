import os


from database.db import db
from base_app import create_app
from resources.ride import blp as RideBlueprint


API_NAME = "Rides MS."
BLUEPRINTS = [RideBlueprint]


if __name__ == "__main__":
    app = create_app(API_NAME, blueprints=BLUEPRINTS)

    app.run(host="0.0.0.0", port=os.getenv("RIDES_API_PORT"))
