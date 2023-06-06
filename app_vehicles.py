import os

from db import db
from base_app import create_app
from resources.vehicle import blp as VehicleBlueprint


API_NAME = "Vehicles MS."
BLUEPRINTS = [VehicleBlueprint]

if __name__ == "__main__":
    app = create_app(API_NAME, blueprints=BLUEPRINTS)

    app.run(host="0.0.0.0", port=os.getenv("VEHICLES_API_PORT"))