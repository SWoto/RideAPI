import json
import uuid

from tests.base_test import UserBaseTest
from src.models import UserModel, UserRoleModel
from src.schemas import UserRoleSchema


class UserTest(UserBaseTest):

    def test_register_user(self):
        data_in = UserTest.default_data_in.copy()
        data_out = UserTest.default_data_out.copy()

        with self.app() as client:
            with self.app_context():

                request = client.post('/', json=data_in)

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
                request = client.post('/', json=data_in)

                received = json.loads(request.data)
                received.pop('id')

                self.assertDictEqual(data_out, received)

                request = client.post('/', json=data_in)

                self.assertEqual(request.status_code, 409)
                self.assertEqual(
                    "An user with that email already exists.", json.loads(request.data)['message'])

    def test_get_user(self):
        data_in = UserTest.default_data_in.copy()
        data_out = UserTest.default_data_out.copy()

        with self.app() as client:
            with self.app_context():
                # test without registering
                request = client.get('/{}'.format(uuid.uuid4().hex))
                self.assertEqual(request.status_code, 404)
                self.assertEqual(json.loads(request.data)[
                                 'status'], "Not Found")

                # request to test again
                request = client.post('/', json=data_in)

                id = json.loads(request.data)['id']
                request = client.get('/{}'.format(id))

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
                request = client.delete('/{}'.format(uuid.uuid4().hex))
                self.assertEqual(request.status_code, 401)
                self.assertEqual(json.loads(request.text)[
                                 "msg"], "Missing Authorization Header")

                request = client.post('/', json=data_in)
                id = json.loads(request.data)['id']

                data_in_login_ok = {
                    'email': data_in['email'],
                    'password': data_in['password'],
                }
                request = client.post('/login', json=data_in_login_ok)
                jwt = json.loads(request.data)['access_token']
                
                request = client.delete('/{}'.format(id), headers={'Authorization': 'Bearer {}'.format(jwt)})

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
                client.post('/', json=data_in_register)

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
                client.post('/', json=data_in_register)

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
                client.post('/', json=data_in_register)

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
                client.post('/', json=data_in_register)

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

    def test_get_all_users(self):
        users_cnt=5
        data_in_register = UserTest.default_data_in.copy()
        data_out_register = UserTest.default_data_out.copy()
        data_in_register_multi_users = []
        data_out_register_multi_users = []
        for i in range(0, users_cnt):
            data_tmp_in = data_in_register.copy()
            data_tmp_in['email'] = "test_{}@rideapi.com".format(i)
            data_in_register_multi_users.append(data_tmp_in)

            data_tmp_out = data_out_register.copy()
            data_tmp_out['email'] = "test_{}@rideapi.com".format(i)
            data_out_register_multi_users.append(data_tmp_out)

        with self.app() as client:
            with self.app_context():
                for i in range(0, users_cnt):
                    request = client.post(
                        '/', json=data_in_register_multi_users[i])
                    data_out_register_multi_users[i]['id'] = json.loads(request.data)[
                        'id']

                data_login = {
                    'email': data_in_register_multi_users[0]['email'],
                    'password': data_in_register_multi_users[0]['password'],
                }
                request = client.post(
                    '/login', json=data_login)
                jwt = json.loads(request.data)['access_token']

                request = client.get(
                    '/', headers={'Authorization': 'Bearer {}'.format(jwt)})

                self.assertListEqual(
                    data_out_register_multi_users, json.loads(request.data))

    def test_get_user_role(self):
        with self.app() as client:
            with self.app_context():
                all_roles = UserRoleModel.query.all()
                for role in all_roles:
                    request = client.get('/role/{}'.format(role.id))
                    self.assertDictEqual(UserRoleSchema().dump(role),
                                         json.loads(request.data))

    def test_get_all_user_roles(self):
         with self.app() as client:
            with self.app_context():
                all_roles = [UserRoleSchema().dump(role) for role in UserRoleModel.query.all()]
                request = client.get('/role')
                self.assertListEqual(all_roles, json.loads(request.data))

    
    def test_register_user_role(self):
        data_in_register = UserTest.default_data_in.copy()

        data_in_login = {
            'email': data_in_register['email'],
            'password': data_in_register['password'],
        }

        with self.app() as client:
            with self.app_context():
                client.post('/', json=data_in_register)

                request = client.post('/login', json=data_in_login)
                jwt = json.loads(request.data)['access_token']

                request = client.post('/role/register', json={'name':'test_register_role'}, headers={'Authorization': 'Bearer {}'.format(jwt)})
                self.assertEqual("test_register_role", json.loads(request.data)['name'])