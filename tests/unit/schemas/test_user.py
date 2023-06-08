import unittest

from src.schemas import PlainUserSchema


class UserPlainSchemaTest(unittest.TestCase):
    data_in = {
        'username': 'test_user',
        'email': 'test@restapi.com',
        'password': 'test_secure'
    }

    def test_load(self):
        schema = PlainUserSchema()
        schema.load(UserPlainSchemaTest.data_in)

    def test_dump(self):
        data_in = UserPlainSchemaTest.data_in.copy()
        data_out = UserPlainSchemaTest.data_in.copy()

        data_out.pop("password")

        schema = PlainUserSchema()

        self.assertEqual(data_out, schema.dump(data_in))
