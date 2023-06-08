import unittest

from src.models import VehicleModel


FAILURE_CONTRUCT_ARGUMENT =  "The {} after creation does not equal the constructor argument."


class VehicleTest(unittest.TestCase):
    def test_create_vehicle(self):
        vehicle_data = {
            "consumption": 11.55,
            "license_plate": "ABC0D12",
            "manufacturer": "Chevrolet",
            "model": "Onix",
        }
        vehicle = VehicleModel(**vehicle_data)

        self.assertEqual(vehicle.consumption, vehicle_data["consumption"], FAILURE_CONTRUCT_ARGUMENT.format("consumption"))
        self.assertEqual(vehicle.license_plate, vehicle_data["license_plate"], FAILURE_CONTRUCT_ARGUMENT.format("license_plate"))
        self.assertEqual(vehicle.manufacturer, vehicle_data["manufacturer"], FAILURE_CONTRUCT_ARGUMENT.format("manufacturer"))
        self.assertEqual(vehicle.model, vehicle_data["model"], FAILURE_CONTRUCT_ARGUMENT.format("model"))
