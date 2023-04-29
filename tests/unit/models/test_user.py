import unittest
from passlib.hash import pbkdf2_sha256

from models import UserModel

FAILURE_CONTRUCT_ARGUMENT =  "The {} after creation does not equal the constructor argument."

class UserTest(unittest.TestCase):
    def test_create_user(self):
        _password = pbkdf2_sha256.hash('test_secure')
        user = UserModel(username='test_user',
                         email='test@restapi.com',
                         password=_password,
                         role=0)

        self.assertEqual(user.username,'test_user', FAILURE_CONTRUCT_ARGUMENT.format('username'))
        self.assertEqual(user.email,'test@restapi.com', FAILURE_CONTRUCT_ARGUMENT.format('email'))
        self.assertEqual(user.password,_password, FAILURE_CONTRUCT_ARGUMENT.format('password'))
        self.assertEqual(user.role,0, FAILURE_CONTRUCT_ARGUMENT.format('role'))