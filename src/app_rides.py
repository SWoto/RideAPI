import os

from base_app import create_app
from resources import RideBlueprint, BaseBlueprint

API_NAME = "Rides MS."
BLUEPRINTS = [BaseBlueprint, RideBlueprint]

if os.getenv("UNITTEST", "-1") != "1":
    app = create_app(api_name=API_NAME, blueprints=BLUEPRINTS)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT"))
