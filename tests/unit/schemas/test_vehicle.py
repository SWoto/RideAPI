import uuid
import unittest
from marshmallow.exceptions import ValidationError

from src.schemas import PlainVehicleSchema


class VehiclePlainSchemaTest(unittest.TestCase):
    data_in = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix",
    }

    def test_load(self):
        schema = PlainVehicleSchema()
        schema.load(VehiclePlainSchemaTest.data_in)

    def test_load_invalid_consuption(self):
        data_in = VehiclePlainSchemaTest.data_in.copy()
        data_in['consumption'] = -5
        schema = PlainVehicleSchema()
        self.assertRaises(ValidationError, schema.load, data_in)

    def test_load_invalid_license_plate(self):
        data_in = VehiclePlainSchemaTest.data_in.copy()
        data_in['license_plate'] = "123"
        schema = PlainVehicleSchema()
        self.assertRaises(ValidationError, schema.load, data_in)

    def test_load_with_id(self):
        data_in = VehiclePlainSchemaTest.data_in.copy()
        data_in["id"] = uuid.uuid4().hex

        schema = PlainVehicleSchema()

        self.assertRaises(ValidationError, schema.load, data_in)

    def test_dump(self):
        data_in = VehiclePlainSchemaTest.data_in.copy()
        data_in["id"] = uuid.uuid4().hex

        schema = PlainVehicleSchema()

        self.assertEqual(data_in, schema.dump(
            data_in))
