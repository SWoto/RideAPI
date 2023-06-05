from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from models import RideModel, UserModel
from schemas import RideSchema


blp = Blueprint("Rides", "rides", description="Operation on rides. Connects drivers and users.")

@blp.route("/register")
class RideRegister(MethodView):
    @jwt_required()
    @blp.arguments(RideSchema)
    @blp.response(201, RideSchema)
    def post(self, ride_data):
        driver = UserModel.find_driver_by_id(ride_data['driver_id'])
        user = UserModel.find_user_by_id(ride_data['user_id'])

        if not driver:
            abort(404, message="Driver not found")

        if not user:
            abort(404, message="User not found")

        ride = RideModel(**ride_data)
        ride.save_to_db()


        return ride
