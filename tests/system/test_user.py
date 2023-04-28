import json

from tests.base_test import BaseTest
from models.user import UserModel
from db import db


class UserTest(BaseTest):
    def test_register_user(self):
        data_in = {'username': 'test_user',
                   'email': 'test@restapi.com',
                   'password': 'test_secure',
                   'role': 0}

        with self.app() as client:
            with self.app_context():
                request = client.post('/register', json=data_in)

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.query.filter(UserModel.email == 'test@restapi.com').first(),
                                     "Did not find an user with email 'test@restapi.com' after posting into endpoint")
                self.assertDictEqual(
                    {"message": "User created succefully."}, json.loads(request.data))

                request = client.post('/register', json=data_in)

                self.assertEqual(request.status_code, 409)
                self.assertEqual(
                    "An user with that email already exists.", json.loads(request.data)['message'])
