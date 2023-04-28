from passlib.hash import pbkdf2_sha256


from tests.base_test import BaseTest
from models.user import UserModel
from db import db


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            _password = pbkdf2_sha256.hash('test_secure')
            user = UserModel(username='test_user',
                             email='test@restapi.com',
                             password=_password,
                             role=0)

            self.assertIsNone(UserModel.query.filter(UserModel.email == 'test@restapi.com').first(),
                              "Found an user with email 'test@restapi.com' before save_to_db")

            db.session.add(user)
            db.session.commit()

            self.assertIsNotNone(UserModel.query.filter(UserModel.email == 'test@restapi.com').first(),
                                 "Did not find an user with email 'test@restapi.com' after save_to_db")

            db.session.delete(user)
            db.session.commit()

            self.assertIsNone(UserModel.query.filter(UserModel.email == 'test@restapi.com').first(),
                              "Found an user with email 'test@restapi.com' after delete_from_db")