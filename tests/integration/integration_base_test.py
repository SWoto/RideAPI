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

    def setUp(self):
        self._app = create_app(BaseTest.SQLALCHEMY_DATABASE_URI)
        with self._app.app_context():
            db.create_all()
        self.app = self._app.test_client()
        self.app_context = self._app.app_context

    def tearDown(self):
        with self._app.app_context():
            db.session.remove()
            db.drop_all()
        self.app = None
        self._app = None