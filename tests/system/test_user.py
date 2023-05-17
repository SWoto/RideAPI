import json
import uuid

from tests.base_test import UserBaseTest
from models import UserModel
from db import db


class UserTest(UserBaseTest):

    def test_register_user(self):
        data_in = UserTest.default_data_in.copy()
        data_out = UserTest.default_data_out.copy()

        with self.app() as client:
            with self.app_context():

                request = client.post('/register', json=data_in)

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_email('test@restapi.com'),
                                     "Did not find an user with email 'test@restapi.com' after posting into endpoint")

                received = json.loads(request.data)
                received.pop('id')

                self.assertDictEqual(data_out, received)

    def test_register_duplicated_user(self):
        data_in = UserTest.default_data_in.copy()
        data_out = UserTest.default_data_out.copy()

        with self.app() as client:
            with self.app_context():
                request = client.post('/register', json=data_in)

                received = json.loads(request.data)
                received.pop('id')

                self.assertDictEqual(data_out, received)

                request = client.post('/register', json=data_in)

                self.assertEqual(request.status_code, 409)
                self.assertEqual(
                    "An user with that email already exists.", json.loads(request.data)['message'])

    def test_get_user(self):
        data_in = UserTest.default_data_in.copy()
        data_out = UserTest.default_data_out.copy()

        with self.app() as client:
            with self.app_context():
                # test without registering
                request = client.get('/user/{}'.format(uuid.uuid4().hex))
                self.assertEqual(request.status_code, 404)
                self.assertEqual(json.loads(request.data)[
                                 'status'], "Not Found")

                # request to test again
                request = client.post('/register', json=data_in)

                id = json.loads(request.data)['id']
                request = client.get('/user/{}'.format(id))

                data_out['id'] = id
                self.assertEqual(request.status_code, 200,
                                 "Could not receive user information")
                self.assertDictEqual(json.loads(
                    request.data), data_out, "User received data does not meet standart")

    def test_delete_user(self):
        data_in = UserTest.default_data_in.copy()

        data_expected = UserTest.default_data_out.copy()

        with self.app() as client:
            with self.app_context():
                # test without registering
                request = client.delete('/user/{}'.format(uuid.uuid4().hex))
                self.assertEqual(request.status_code, 404)
                self.assertEqual(json.loads(request.data)[
                                 'status'], "Not Found")

                request = client.post('/register', json=data_in)

                id = json.loads(request.data)['id']
                request = client.delete('/user/{}'.format(id))

                data_expected['id'] = id
                self.assertEqual(request.status_code, 200,
                                 "Could not delete user")
                self.assertEqual(json.loads(request.data)[
                                 'message'], "User deleted.")

    def test_register_and_login(self):
        data_in_register = UserTest.default_data_in.copy()

        data_in_login_ok = {
            'email': 'test@restapi.com',
            'password': 'test_secure',
        }

        with self.app() as client:
            with self.app_context():
                # test without registering
                client.post('/register', json=data_in_register)

                request = client.post('/login', json=data_in_login_ok)
                self.assertIn('access_token', json.loads(request.data).keys())

    def test_login_failed(self):
        data_in_register = UserTest.default_data_in.copy()

        data_in_login_bad = {
            'email': 'test@restapi.com',
            'password': 'abcdefgh',
        }

        with self.app() as client:
            with self.app_context():
                # test without registering
                client.post('/register', json=data_in_register)

                request = client.post('/login', json=data_in_login_bad)
                self.assertEqual(request.status_code, 401)
                self.assertEqual(json.loads(request.data)[
                                 'message'], "Invalid credentials.")

    def test_login_logout(self):
        data_in_register = UserTest.default_data_in.copy()

        data_in_login = {
            'email': 'test@restapi.com',
            'password': 'test_secure',
        }

        with self.app() as client:
            with self.app_context():
                # test without registering
                client.post('/register', json=data_in_register)

                request = client.post('/login', json=data_in_login)
                jwt = json.loads(request.data)['access_token']

                request = client.delete(
                    '/logout', headers={'Authorization': 'Bearer {}'.format(jwt)})
                self.assertEqual(json.loads(request.data)[
                                 'message'], "Successfully logged out.")

    def test_duplicated_logout(self):
        data_in_register = UserTest.default_data_in.copy()

        data_in_login = {
            'email': 'test@restapi.com',
            'password': 'test_secure',
        }

        with self.app() as client:
            with self.app_context():
                # test without registering
                client.post('/register', json=data_in_register)

                request = client.post('/login', json=data_in_login)
                jwt = json.loads(request.data)['access_token']

                request = client.delete(
                    '/logout', headers={'Authorization': 'Bearer {}'.format(jwt)})
                self.assertEqual(json.loads(request.data)[
                                 'message'], "Successfully logged out.")

                request = client.delete(
                    '/logout', headers={'Authorization': 'Bearer {}'.format(jwt)})
                self.assertEqual(json.loads(request.data)[
                                 'description'], "The token has been revoked.")
