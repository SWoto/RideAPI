import unittest
import uuid
from marshmallow.exceptions import ValidationError

from schemas import PlainUserSchema


class UserPlainSchemaTest(unittest.TestCase):
    data_in = {
        'username': 'test_user',
        'email': 'test@restapi.com',
        'password': 'test_secure',
        'role': 0,
    }

    def test_load(self):
        schema = PlainUserSchema()
        loaded = schema.load(UserPlainSchemaTest.data_in)

    def test_load_with_id(self):
        data_in = UserPlainSchemaTest.data_in.copy()
        data_in["id"] = uuid.uuid4().hex

        schema = PlainUserSchema()

        self.assertRaises(ValidationError, schema.load, data_in)


    def test_dump(self):
        data_in = UserPlainSchemaTest.data_in.copy()
        data_out = UserPlainSchemaTest.data_in.copy()

        _id = uuid.uuid4().hex
        data_in["id"] = _id
        data_out["id"] = _id

        data_out.pop("password")

        schema = PlainUserSchema()
        
        self.assertEqual(data_out, schema.dump(data_in))