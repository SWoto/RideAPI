import uuid
import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt, jwt_required

from db import db
from models import VehicleModel
from schemas import VehicleSchema


blp = Blueprint("Vehicles", "vehicles",
                description="Operation os vehicles. Register them to users and rides.")


#TODO: Add test
@blp.route("/register")
class VehicleRegister(MethodView):

    @jwt_required()
    @blp.arguments(VehicleSchema)
    @blp.response(201, VehicleSchema)
    def post(self, vehicle_data):
        if VehicleModel.find_by_license_plate(vehicle_data['license_plate']):
            abort(409, message="A vehicle with that license plate already exists")

        vehicle = VehicleModel(**vehicle_data)
        vehicle.save_to_db()
        return vehicle
        

