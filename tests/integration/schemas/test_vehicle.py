import unittest
import uuid
from schemas import VehicleSchema


class VehicleSchemaTest(unittest.TestCase):
    data_in = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix",
        "user_id": uuid.uuid4().hex,
    }

    data_out = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix",
        "id": uuid.uuid4().hex,
        "user": {
            "email": "test@restapi.com",
            "id": uuid.uuid4().hex,
            "username": "test_user",
        }
    }

    def test_load(self):
        schema = VehicleSchema()
        schema.load(VehicleSchemaTest.data_in)

    def test_dump(self):
        schema = VehicleSchema()
        self.assertEqual(VehicleSchemaTest.data_out,
                         schema.dump(VehicleSchemaTest.data_out))
