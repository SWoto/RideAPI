import uuid
import unittest
import random
from marshmallow.exceptions import ValidationError

from src.schemas import PlainRideSchema


class RidePlainSchemaTest(unittest.TestCase):
    data_in = {
        "distance": random.randint(1, 19999)/100,
        "gas_price": random.randint(1, 4999)/100,
    }

    def test_load(self):
        schema = PlainRideSchema()
        schema.load(RidePlainSchemaTest.data_in)

    def test_load_invalid_distance(self):
        data_in = RidePlainSchemaTest.data_in.copy()
        data_in['distance'] = 0
        schema = PlainRideSchema()
        self.assertRaises(ValidationError, schema.load, data_in)

        data_in['distance'] = 200
        schema = PlainRideSchema()
        self.assertRaises(ValidationError, schema.load, data_in)

    def test_load_invalid_license_plate(self):
        data_in = RidePlainSchemaTest.data_in.copy()
        data_in['gas_price'] = 0
        schema = PlainRideSchema()
        self.assertRaises(ValidationError, schema.load, data_in)

        data_in['gas_price'] = 50
        schema = PlainRideSchema()
        self.assertRaises(ValidationError, schema.load, data_in)

    def test_load_with_id(self):
        data_in = RidePlainSchemaTest.data_in.copy()
        data_in["id"] = uuid.uuid4().hex

        schema = PlainRideSchema()

        self.assertRaises(ValidationError, schema.load, data_in)

    def test_dump(self):
        data_in = RidePlainSchemaTest.data_in.copy()
        data_in["id"] = uuid.uuid4().hex
        data_in["total_value"] = 20

        schema = PlainRideSchema()

        self.assertEqual(data_in, schema.dump(
            data_in))
