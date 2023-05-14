"""
BaseTest

This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

import unittest

from db import db
from base_app import create_app
from models.user import UserModel
from models.vehicle import VehicleModel
from app_users import API_NAME as USER_API_NAME, BLUEPRINTS as USER_BLUEPRINTS
from app_vehicles import API_NAME as VEHICLES_API_NAME, BLUEPRINTS as VEHICLES_BLUEPRINTS


class BaseTest(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"

    @classmethod
    def setUpClass(cls):
        cls._app = create_app(
            cls.API_NAME, blueprints=cls.BLUEPRINTS, db_url=BaseTest.SQLALCHEMY_DATABASE_URI)

    @classmethod
    def tearDownClass(cls):
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


class VehiclesBaseTest(BaseTest):
    API_NAME = VEHICLES_API_NAME
    BLUEPRINTS = VEHICLES_BLUEPRINTS

    vehicle_data = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix"
    }


    def setUp(self):
        super(VehiclesBaseTest, self).setUp()
        with self.app_context():
            data_in = {
                'username': 'test_user',
                'email': 'test@restapi.com',
                'password': 'test_secure',
                'role': 0,
            }
            user = UserModel(**data_in)
            user.save_to_db()
            
            VehiclesBaseTest.vehicle_data["user_id"] = user.id

