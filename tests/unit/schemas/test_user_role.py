import unittest
import uuid

from schemas import UserRoleSchema


class RoleSchemaTest(unittest.TestCase):
    data_in = {"name": "test_user_role"}

    def test_load(self):
        schema = UserRoleSchema()
        schema.load(RoleSchemaTest.data_in)

    def test_dump(self):
        data_in = RoleSchemaTest.data_in.copy()
        data_in['id'] = uuid.uuid4().hex
        schema = UserRoleSchema()
        dump = schema.dump(data_in)
        self.assertEqual(data_in, dump)