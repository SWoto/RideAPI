from passlib.hash import pbkdf2_sha256
import uuid

from src.models import UserModel
from tests.base_test import UserBaseTest

FAILURE_CONTRUCT_ARGUMENT =  "The {} after creation does not equal the constructor argument."

class UserTest(UserBaseTest):
    def test_create_user(self):
        data_in = UserTest.default_data_in.copy()
        user = UserModel(**data_in)

        self.assertEqual(uuid.UUID(user.id).version, 4)
        self.assertEqual(user.username,data_in['username'], FAILURE_CONTRUCT_ARGUMENT.format('username'))
        self.assertEqual(user.email,data_in['email'], FAILURE_CONTRUCT_ARGUMENT.format('email'))
        self.assertTrue(pbkdf2_sha256.verify(data_in['password'], user.password), FAILURE_CONTRUCT_ARGUMENT.format('password'))
        self.assertEqual(user.role_id,data_in['role_id'], FAILURE_CONTRUCT_ARGUMENT.format('role'))