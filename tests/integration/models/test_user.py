from tests.base_test import UserBaseTest
from src.models import UserModel

FAILED_TO_FIND_USER_WITH = "Did not find an user with {} '{}'"
FAILED_DUPLICATED = "Duplicated - user {} was previusly added to the database"
FAILED_SAVE_TO_DB = "Did not find user '{}' after save_to_db"
FAILED_DELETE_FROM_DB = "Found user '{}' after delete_from_db"


class UserTest(UserBaseTest):
    def test_save_to_db(self):
        user = UserModel(**UserTest.default_data_in)

        with self.app_context():
            user.save_to_db()

            self.assertIsNotNone(UserModel.query.filter_by(
                id=user.id).first(), FAILED_SAVE_TO_DB.format(user.email))

    def test_delete_from_db(self):
        user = UserModel(**UserTest.default_data_in)

        with self.app_context():
            user.save_to_db()

            self.assertIsNotNone(UserModel.query.filter_by(
                id=user.id).first(), FAILED_SAVE_TO_DB.format(user.email))

            user.delete_from_db()
            self.assertIsNone(UserModel.query.filter_by(
                id=user.id).first(), FAILED_DELETE_FROM_DB.format(user.email))

    def test_find_by_id(self):
        user = UserModel(**UserTest.default_data_in)

        with self.app_context():
            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_id(
                user.id), FAILED_TO_FIND_USER_WITH.format("id", user.id))

    def test_find_by_email(self):
        user = UserModel(**UserTest.default_data_in)

        with self.app_context():
            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_email(
                user.email), FAILED_TO_FIND_USER_WITH.format("email", user.email))

    def test_crud(self):
        user = UserModel(**UserTest.default_data_in)
        email = user.email
        with self.app_context():

            self.assertIsNone(user.find_by_email(email),
                              FAILED_DUPLICATED.format(email))

            user.save_to_db()

            self.assertIsNotNone(user.find_by_email(email),
                                 FAILED_SAVE_TO_DB.format(email))

            user.delete_from_db()

            self.assertIsNone(user.find_by_email(email),
                              FAILED_DELETE_FROM_DB.format(email))
