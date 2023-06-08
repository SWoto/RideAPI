from tests.base_test import VehiclesBaseTest
from src.models import VehicleModel

FAILED_TO_FIND_VEHICLE_WITH = "Did not find a vehicle with {} '{}'"
FAILED_DUPLICATED = "Duplicated - vehicle {} was previusly added to the database"
FAILED_SAVE_TO_DB = "Did not find vehicle '{}' after save_to_db"
FAILED_DELETE_FROM_DB = "Found vehicle '{}' after delete_from_db"


class VehicleTest(VehiclesBaseTest):
    def test_save_to_db(self):
        vehicle = VehicleModel(**VehicleTest.vehicle_data_in)

        with self.app_context():
            vehicle.save_to_db()
            self.assertIsNotNone(VehicleModel.query.filter_by(
                id=vehicle.id).first(), FAILED_SAVE_TO_DB.format(vehicle.license_plate))

    def test_delete_from_db(self):
        vehicle = VehicleModel(**VehicleTest.vehicle_data_in)

        with self.app_context():
            vehicle.save_to_db()
            self.assertIsNotNone(VehicleModel.query.filter_by(
                id=vehicle.id).first(), FAILED_SAVE_TO_DB.format(vehicle.license_plate))

            vehicle.delete_from_db()
            self.assertIsNone(VehicleModel.query.filter_by(
                id=vehicle.id).first(), FAILED_DELETE_FROM_DB.format(vehicle.license_plate))

    def test_find_by_id(self):
        vehicle = VehicleModel(**VehicleTest.vehicle_data_in)

        with self.app_context():
            vehicle.save_to_db()
            self.assertIsNotNone(VehicleModel.find_by_id(vehicle.id), FAILED_TO_FIND_VEHICLE_WITH.format("license_plate", vehicle.license_plate))

    def test_find_by_license_plate(self):
        vehicle = VehicleModel(**VehicleTest.vehicle_data_in)

        with self.app_context():
            vehicle.save_to_db()
            self.assertIsNotNone(VehicleModel.find_by_license_plate(vehicle.license_plate), FAILED_TO_FIND_VEHICLE_WITH.format("license_plate", vehicle.license_plate))


    def test_crud(self):
        vehicle = VehicleModel(**VehicleTest.vehicle_data_in)

        with self.app_context():
            self.assertIsNone(VehicleModel.query.filter_by(
                id=vehicle.id).first(), FAILED_DUPLICATED.format(vehicle.license_plate))
            
            vehicle.save_to_db()

            self.assertIsNotNone(VehicleModel.query.filter_by(
                id=vehicle.id).first(), FAILED_SAVE_TO_DB.format(vehicle.license_plate))
            

            vehicle.delete_from_db()
            
            self.assertIsNone(VehicleModel.query.filter_by(
                id=vehicle.id).first(), FAILED_DELETE_FROM_DB.format(vehicle.license_plate))
