from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from models import RideModel, UserModel, VehicleModel
from schemas import RideSchema


blp = Blueprint("Rides", "rides", description="Operation on rides. Connects drivers and users.")

@blp.route("/register")
class RideRegister(MethodView):
    @jwt_required()
    @blp.arguments(RideSchema)
    @blp.response(201, RideSchema)
    def post(self, ride_data):
        driver = UserModel.find_driver_by_id(ride_data['driver_id'])
        passanger = UserModel.find_passanger_by_id(ride_data['passanger_id'])
        active_vehicle = VehicleModel.get_user_active_vehicles(ride_data['driver_id'])

        if not driver:
            abort(404, message="Driver not found")

        if not active_vehicle:
            abort(404, message="Driver has no active vehicle")

        if len(active_vehicle) > 1:
            return abort(405,  message="Driver has more than one active vehicle")

        if not passanger:
            abort(404, message="Passanger not found")

        active_vehicle = active_vehicle[0]
        price = ride_data['distance']/float(active_vehicle.consumption)*ride_data['gas_price']
        
        ride_data["total_value"] = price
        ride = RideModel(**ride_data)
        ride.save_to_db()


        return ride

