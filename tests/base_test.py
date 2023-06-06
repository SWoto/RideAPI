"""
BaseTest

This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

import os
import unittest
from flask_jwt_extended import create_access_token

from db import db
from sqlalchemy.sql import text
from base_app import create_app
from models import UserModel, UserRoleModel
from app_users import API_NAME as USER_API_NAME, BLUEPRINTS as USER_BLUEPRINTS
from app_vehicles import API_NAME as VEHICLES_API_NAME, BLUEPRINTS as VEHICLES_BLUEPRINTS


class BaseTest(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = DATABASE_URL = "postgresql://{}:{}@127.0.0.1:5433/{}".format(
            os.getenv(
            "POSTGRES_USER"), os.getenv(
            "POSTGRES_PASSWORD"), os.getenv(
            "POSTGRES_DB"))

    @classmethod
    def setUpClass(cls):
        os.environ["UNITTEST"] = "1"
        cls._app = create_app(
            cls.API_NAME, blueprints=cls.BLUEPRINTS, db_url=BaseTest.SQLALCHEMY_DATABASE_URI)

        # with db.engine.connect() as conn:
        #     expected = [(1, 'test row 1', True), (2, 'test row 2', False)]
        #     result = conn.execute(text("SELECT * FROM public.test"))


    @classmethod
    def tearDownClass(cls):
        os.environ.pop("UNITTEST")
        pass

    def setUp(self):
        with self._app.app_context():
            db.create_all()
        self.app = self._app.test_client
        self.app_context = self._app.app_context

    def tearDown(self):
        with self._app.app_context():
            db.session.remove()
            db.drop_all()


class UserBaseTest(BaseTest):
    API_NAME = USER_API_NAME
    BLUEPRINTS = USER_BLUEPRINTS

    default_data_in = {
        'username': 'test_user',
        'email': 'test@restapi.com',
        'password': 'test_secure',
        'role_id': "",
    }

    default_data_out = {
        'username': 'test_user',
        'email': 'test@restapi.com',
        'role': {},
        'vehicles': [],
    }

    def setUp(self):
        super(UserBaseTest, self).setUp()
        with self.app_context():
            UserBaseTest.set_role()


    @classmethod
    def set_role(cls):
        role_info = {"name": "test_role"}   
        role = UserRoleModel(**role_info)
        role.save_to_db()

        role_info['id'] = role.id
        cls.default_data_in['role_id'] = role.id
        cls.default_data_out['role'] = role_info.copy()



class VehiclesBaseTest(BaseTest):
    API_NAME = VEHICLES_API_NAME
    BLUEPRINTS = VEHICLES_BLUEPRINTS

    vehicle_data_in = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix",
        "user_id":"",
    }

    #note that ID is missing
    vehicle_data_out = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix",
        "user":{},
    }

    data_user_login_ok = {
            'email': 'test@restapi.com',
            'password': 'test_secure',
        }


    def setUp(self):
        super(VehiclesBaseTest, self).setUp()
        with self.app_context():
            UserBaseTest.set_role()
            user_data_in = UserBaseTest.default_data_in.copy()

            user = UserModel(**user_data_in)
            user.save_to_db()
            
            VehiclesBaseTest.vehicle_data_in["user_id"] = user.id
            VehiclesBaseTest.vehicle_data_out["user"] = {
                "username":user.username,
                "email":user.email,
                "id":user.id,
            }
            self.access_token = create_access_token(identity=user.id, fresh=True)


class UserRoleBaseTest(BaseTest):
    API_NAME = USER_API_NAME
    BLUEPRINTS = USER_BLUEPRINTS

    default_data_in = {
        'name': 'test_user_role',
    }

