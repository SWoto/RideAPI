import uuid
import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt, jwt_required

from db import db
from models import VehicleModel, UserModel
from schemas import VehicleSchema


blp = Blueprint("Vehicles", "vehicles",
                description="Operation os vehicles. Register them to users and rides.")


@blp.route("/register")
class VehicleRegister(MethodView):

    @jwt_required()
    @blp.arguments(VehicleSchema)
    @blp.response(201, VehicleSchema)
    def post(self, vehicle_data):
        if VehicleModel.find_by_license_plate(vehicle_data['license_plate']):
            abort(409, message="A vehicle with that license plate already exists")

        if not UserModel.find_by_id(vehicle_data['user_id']):
            abort(404, message="User not found")

        vehicle = VehicleModel(**vehicle_data)
        vehicle.save_to_db()
        return vehicle


# TODO: Add to postman
@blp.route("/vehicle/<string:vehicle_id>")
class Vehicle(MethodView):

    @blp.response(200, VehicleSchema)
    def get(self, vehicle_id):
        return VehicleModel.query.get_or_404(vehicle_id)


    @jwt_required()
    def delete(self, vehicle_id):
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        vehicle.delete_from_db()
        return {"message": "User deleted."}, 200


@blp.route("/vehicle")
class VehicleList(MethodView):

    @jwt_required()
    @blp.response(200, VehicleSchema(many=True))
    def get(self):
        print(VehicleModel.query.all())
        return VehicleModel.query.all()


