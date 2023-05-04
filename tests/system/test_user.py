import json
import uuid

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

                received = json.loads(request.data)
                received.pop('id')
                data_in_wo_password = data_in.copy()
                data_in_wo_password.pop('password')

                self.assertDictEqual(data_in_wo_password, received)

                request = client.post('/register', json=data_in)

                self.assertEqual(request.status_code, 409)
                self.assertEqual(
                    "An user with that email already exists.", json.loads(request.data)['message'])

    def test_get_user(self):
        data_in = {'username': 'test_user',
                   'email': 'test@restapi.com',
                   'password': 'test_secure',
                   'role': 0}
        
        data_expected = data_in.copy()
        data_expected.pop('password')

        with self.app() as client:
            with self.app_context():
                #test without registering
                request = client.get('/user/{}'.format(uuid.uuid4().hex))
                self.assertEqual(request.status_code, 404)
                self.assertEqual(json.loads(request.data)['message'], "There is no user with requested id")

                # request to test again
                request = client.post('/register', json=data_in)

                id = json.loads(request.data)['id']
                request = client.get('/user/{}'.format(id))

                data_expected['id'] = id
                self.assertEqual(request.status_code, 200, "Could not receive user information")
                self.assertDictEqual(json.loads(request.data), data_expected, "User received data does not meet standart")

    def test_delete_user(self):
        data_in = {'username': 'test_user',
            'email': 'test@restapi.com',
            'password': 'test_secure',
            'role': 0}
        
        data_expected = data_in.copy()
        data_expected.pop('password')

        with self.app() as client:
            with self.app_context():
                #test without registering
                request = client.delete('/user/{}'.format(uuid.uuid4().hex))
                self.assertEqual(request.status_code, 404)
                self.assertEqual(json.loads(request.data)['message'], "There is no user with requested id")

                request = client.post('/register', json=data_in)

                id = json.loads(request.data)['id']
                request = client.delete('/user/{}'.format(id))

                data_expected['id'] = id
                self.assertEqual(request.status_code, 200, "Could not delete user")
                self.assertEqual(json.loads(request.data)['message'], "User deleted")
