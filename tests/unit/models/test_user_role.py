import unittest
import uuid

from models import UserRoleModel

class UserRoleTest(unittest.TestCase):
    def test_create_role(self):
        role = UserRoleModel(name="test_user_role")

        self.assertEqual(role.name, "test_user_role")
        self.assertEqual(uuid.UUID(role.id).version, 4)