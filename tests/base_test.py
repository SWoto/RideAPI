"""
BaseTest

This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

import unittest

from app_users import create_app
from db import db

class BaseTest(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"

    @classmethod
    def setUpClass(cls):
        cls._app = create_app(BaseTest.SQLALCHEMY_DATABASE_URI)

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