import unittest
import uuid
from marshmallow.exceptions import ValidationError

from schemas import UserSchema


class UserSchemaTest(unittest.TestCase):
    def test_user_schema_load(self):
        schema = UserSchema()
        _id = uuid.uuid4().hex

        data_in = {'id': _id,
                   'username': 'test_user',
                   'email': 'test@restapi.com',
                   'password': 'test_secure',
                   'role': 0}

        # Check for validation error due to id being in it
        self.assertRaises(ValidationError, schema.load, data_in)

        data_in.pop('id')

        # if it do not raise anything, there is no unkown argument
        loaded = schema.load(data_in)

    def test_user_schema_dump(self):
        schema = UserSchema()
        _id = uuid.uuid4().hex

        data_in = {'id': _id,
                   'username': 'test_user',
                   'email': 'test@restapi.com',
                   'password': 'test_secure',
                   'role': 0}

        self.assertIsNone(schema.dump(data_in).get('password'),
                          "Password is being returned from the schema")
        data_in.pop('password')

        self.assertDictEqual(data_in, schema.dump(data_in))
