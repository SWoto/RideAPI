import unittest
import uuid

from schemas import UserSchema


class UserSchemaTest(unittest.TestCase):
    data_in = {
        'username': 'test_user',
        'email': 'test@restapi.com',
        'password': 'test_secure',
        'role': 0,
    }

    data_out = {
        'username': 'test_user',
        'email': 'test@restapi.com',
        'role': 0,
        'id': uuid.uuid4().hex,
        'vehicles': [],
    }

    def test_load(self):
        schema = UserSchema()
        schema.load(UserSchemaTest.data_in)

    def test_dump(self):
        schema = UserSchema()
        self.assertEqual(UserSchemaTest.data_out, schema.dump(
            UserSchemaTest.data_out), "Failed to dump data through schema")

    def test_dump_with_vechile(self):
        data_out = UserSchemaTest.data_out.copy()
        data_out['vehicles'] = [
            {
                "consumption": 11.55,
                "license_plate": "ABC0D12",
                "manufacturer": "Chevrolet",
                "model": "Onix",
                "id": uuid.uuid4().hex,
            }
        ]

        schema = UserSchema()

        self.assertEqual(UserSchemaTest.data_out, schema.dump(
            UserSchemaTest.data_out), "Failed to dump data through schema")

    def test_dump_with_multi_vechiles(self):
        data_out = UserSchemaTest.data_out.copy()
        data_out['vehicles'] = [
            {
                "consumption": 11.55,
                "license_plate": "ABC0D12",
                "manufacturer": "Chevrolet",
                "model": "Onix",
                "id": uuid.uuid4().hex,
            },
            {
                "consumption": 13.99,
                "license_plate": "DEF0D41",
                "manufacturer": "Chevrolet2",
                "model": "Onix2",
                "id": uuid.uuid4().hex,
            },
        ]

        schema = UserSchema()

        self.assertEqual(UserSchemaTest.data_out, schema.dump(
            UserSchemaTest.data_out), "Failed to dump data through schema")
