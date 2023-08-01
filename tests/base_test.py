"""
BaseTest

This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

import os
import random
import unittest
from flask_jwt_extended import create_access_token

import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "src"
)
sys.path.append(SOURCE_PATH)

os.environ["UNITTEST"] = "1"

from src.app_vehicles import API_NAME as VEHICLES_API_NAME, BLUEPRINTS as VEHICLES_BLUEPRINTS
from src.app_users import API_NAME as USER_API_NAME, BLUEPRINTS as USER_BLUEPRINTS
from src.app_rides import API_NAME as RIDES_API_NAME, BLUEPRINTS as RIDES_BLUEPRINT
from src.models import UserModel, UserRoleModel, VehicleModel
from src.base_app import create_app, db


class BaseTest(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
            os.getenv("POSTGRES_USER"), 
            os.getenv("POSTGRES_PASSWORD"),
            os.getenv("POSTGRES_TEST_HOST", "127.0.0.1"),
            os.getenv("POSTGRES_TEST_PORT", "5433"), 
            os.getenv("POSTGRES_DB"),
        )

    @classmethod
    def setUpClass(cls):
        print("setUpClass: ", BaseTest.SQLALCHEMY_DATABASE_URI)
        cls._app = create_app(
            api_name=cls.API_NAME, blueprints=cls.BLUEPRINTS, db_url=BaseTest.SQLALCHEMY_DATABASE_URI, test_mode=True)
        # with db.engine.connect() as conn:
        #     expected = [(1, 'test row 1', True), (2, 'test row 2', False)]
        #     result = conn.execute(text("SELECT * FROM public.test"))

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

    default_data_passenger = {
        'username': 'test_passenger',
        'email': 'passenger@restapi.com',
        'password': 'test_secure',
        'role_id': "",
    }

    default_data_driver = {
        'username': 'test_driver',
        'email': 'driver@restapi.com',
        'password': 'test_secure',
        'role_id': "",
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

    @classmethod
    def set_passenger_rider(cls):
        role_info = {"name": "passenger"}
        role = UserRoleModel(**role_info)
        role.save_to_db()
        cls.default_data_passenger['role_id'] = role.id

        role_info = {"name": "driver"}
        role = UserRoleModel(**role_info)
        role.save_to_db()
        cls.default_data_driver['role_id'] = role.id


class VehiclesBaseTest(BaseTest):
    API_NAME = VEHICLES_API_NAME
    BLUEPRINTS = VEHICLES_BLUEPRINTS

    vehicle_data_in = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix",
        "user_id": "",
    }

    # note that ID is missing
    vehicle_data_out = {
        "consumption": 11.55,
        "license_plate": "ABC0D12",
        "manufacturer": "Chevrolet",
        "model": "Onix",
        "user": {},
    }

    data_user_login_ok = {
        'email': 'test@restapi.com',
        'password': 'test_secure',
    }

    def setUp(self):
        super(VehiclesBaseTest, self).setUp()
        with self.app_context():
            user_id = VehiclesBaseTest.set_vehicle()
            self.access_token = create_access_token(
                identity=user_id, fresh=True)

    @classmethod
    def set_vehicle(self, user=None):
        if not user:
            UserBaseTest.set_role()
            user_data_in = UserBaseTest.default_data_in.copy()

            user = UserModel(**user_data_in)
            user.save_to_db()

        VehiclesBaseTest.vehicle_data_in["user_id"] = user.id
        VehiclesBaseTest.vehicle_data_out["user"] = {
            "username": user.username,
            "email": user.email,
            "id": user.id,
        }

        return user.id


class UserRoleBaseTest(BaseTest):
    API_NAME = USER_API_NAME
    BLUEPRINTS = USER_BLUEPRINTS

    default_data_in = {
        'name': 'test_user_role',
    }


class RideBaseTest(BaseTest):
    API_NAME = RIDES_API_NAME
    BLUEPRINTS = RIDES_BLUEPRINT

    default_data_in = {
        "distance": random.randint(1, 19999)/100,
        "gas_price": random.randint(1, 4999)/100,
        "total_value": random.randint(100, 99999)/100,
        "passenger_id": "",
        "driver_id": "",
    }

    default_data_out = {}

    default_data_in_system = {}

    def setUp(self):
        print(BaseTest.SQLALCHEMY_DATABASE_URI)
        super(RideBaseTest, self).setUp()
        with self.app_context():
            UserBaseTest.set_passenger_rider()
            passenger_data_in = UserBaseTest.default_data_passenger.copy()
            driver_data_in = UserBaseTest.default_data_driver.copy()

            passenger = UserModel(**passenger_data_in)
            passenger.save_to_db()
            driver = UserModel(**driver_data_in)
            driver.save_to_db()

            _ = VehiclesBaseTest.set_vehicle(driver)

            vehicle = VehicleModel(**VehiclesBaseTest.vehicle_data_in, active=True)
            vehicle.save_to_db()

            RideBaseTest.default_data_in["passenger_id"] = passenger.id
            RideBaseTest.default_data_in["driver_id"] = driver.id

            self.access_token = create_access_token(
                identity=passenger.id, fresh=True)


            RideBaseTest.default_data_in_system = RideBaseTest.default_data_in.copy()
            RideBaseTest.default_data_in_system.pop('total_value')

            RideBaseTest.default_data_out = RideBaseTest.default_data_in.copy()
            RideBaseTest.default_data_out.pop('passenger_id')
            RideBaseTest.default_data_out['passenger'] = {
                'email':passenger.email,
                'id':passenger.id,
                'username':passenger.username
            }
            RideBaseTest.default_data_out.pop('driver_id')
            RideBaseTest.default_data_out['driver'] = {
                'email':driver.email,
                'id':driver.id,
                'username':driver.username
            }
            price = round(RideBaseTest.default_data_out['distance'] / \
                VehiclesBaseTest.vehicle_data_in['consumption']*RideBaseTest.default_data_out['gas_price'],2)
            RideBaseTest.default_data_out['total_value']=price