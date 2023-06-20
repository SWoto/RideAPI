import unittest

from src.models import VehicleModel


FAILURE_CONTRUCT_ARGUMENT =  "The {} after creation does not equal the constructor argument."


class VehicleTest(unittest.TestCase):
    def test_create_vehicle(self):
        default_data_in = {
            "consumption": 11.55,
            "license_plate": "ABC0D12",
            "manufacturer": "Chevrolet",
            "model": "Onix",
        }

        vehicle = VehicleModel(**default_data_in)

        self.assertEqual(vehicle.consumption, default_data_in["consumption"], FAILURE_CONTRUCT_ARGUMENT.format("consumption"))
        self.assertEqual(vehicle.license_plate, default_data_in["license_plate"], FAILURE_CONTRUCT_ARGUMENT.format("license_plate"))
        self.assertEqual(vehicle.manufacturer, default_data_in["manufacturer"], FAILURE_CONTRUCT_ARGUMENT.format("manufacturer"))
        self.assertEqual(vehicle.model, default_data_in["model"], FAILURE_CONTRUCT_ARGUMENT.format("model"))