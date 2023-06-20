import unittest
import uuid
import random

from src.schemas import RideSchema


class RideSchemaTest(unittest.TestCase):
    data_in = {
        "distance": random.randint(1, 19999)/100,
        "gas_price": random.randint(1, 4999)/100,
        "passenger_id": uuid.uuid4().hex,
        "driver_id": uuid.uuid4().hex,
    }

    data_out = {
        "distance": random.randint(1, 19999)/100,
        "gas_price": random.randint(1, 4999)/100,
        "total_value": random.randint(1, 999999)/100,
        "id": uuid.uuid4().hex,
        "passenger": {
            "email": "passenger@restapi.com",
            "id": uuid.uuid4().hex,
            "username": "test_passenger",
        },
        "driver": {
            "email": "driver@restapi.com",
            "id": uuid.uuid4().hex,
            "username": "test_driver",
        },
    }

    def test_load(self):
        schema = RideSchema()
        schema.load(RideSchemaTest.data_in)

    def test_dump(self):
        schema = RideSchema()
        self.assertEqual(RideSchemaTest.data_out,
                         schema.dump(RideSchemaTest.data_out))
