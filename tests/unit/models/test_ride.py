import unittest

from src.models import RideModel


FAILURE_CONTRUCT_ARGUMENT =  "The {} after creation does not equal the constructor argument."


class RideTest(unittest.TestCase):
    def test_create_ride(self):
        default_data_in = {
            "distance": 17.99,
            "gas_price": 5.72,
            "total_value": 55.99,
        }

        ride = RideModel(**default_data_in)

        self.assertEqual(ride.distance, default_data_in["distance"], FAILURE_CONTRUCT_ARGUMENT.format("distance"))
        self.assertEqual(ride.gas_price, default_data_in["gas_price"], FAILURE_CONTRUCT_ARGUMENT.format("gas_price"))
        self.assertEqual(ride.total_value, default_data_in["total_value"], FAILURE_CONTRUCT_ARGUMENT.format("total_value"))