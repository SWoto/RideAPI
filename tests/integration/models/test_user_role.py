from tests.base_test import UserRoleBaseTest

from src.models import UserRoleModel

FAILED_TO_FIND_USER_WITH = "Did not find a role with {} '{}'"
FAILED_DUPLICATED = "Duplicated - role {} was previusly added to the database"
FAILED_SAVE_TO_DB = "Did not find role '{}' after save_to_db"
FAILED_DELETE_FROM_DB = "Found role '{}' after delete_from_db"


class UserRoleTest(UserRoleBaseTest):
    def test_save_to_db(self):
        role = UserRoleModel(**UserRoleTest.default_data_in)

        with self.app_context():
            role.save_to_db()
            self.assertIsNotNone(UserRoleModel.query.filter_by(
                id=role.id).first(), FAILED_SAVE_TO_DB.format(role.name))

    def test_delete_from_db(self):
        role = UserRoleModel(**UserRoleTest.default_data_in)

        with self.app_context():
            role.save_to_db()
            self.assertIsNotNone(UserRoleModel.query.filter_by(
                id=role.id).first(), FAILED_SAVE_TO_DB.format(role.name))

            role.delete_from_db()
            self.assertIsNone(UserRoleModel.query.filter_by(
                id=role.id).first(), FAILED_DELETE_FROM_DB.format(role.name))

    def test_find_by_id(self):
        role = UserRoleModel(**UserRoleTest.default_data_in)

        with self.app_context():
            role.save_to_db()

            self.assertIsNotNone(UserRoleModel.find_by_id(
                role.id), FAILED_TO_FIND_USER_WITH.format("id", role.id))

    def test_find_by_name(self):
        role = UserRoleModel(**UserRoleTest.default_data_in)

        with self.app_context():
            role.save_to_db()

            self.assertIsNotNone(UserRoleModel.find_by_name(
                role.name), FAILED_TO_FIND_USER_WITH.format("name", role.name))


    def test_crud(self):
        role = UserRoleModel(**UserRoleTest.default_data_in)
        name = role.name

        with self.app_context():

            self.assertIsNone(role.find_by_name(name),
                              FAILED_DUPLICATED.format(name))

            role.save_to_db()

            self.assertIsNotNone(role.find_by_name(name),
                                 FAILED_SAVE_TO_DB.format(name))

            role.delete_from_db()

            self.assertIsNone(role.find_by_name(name),
                              FAILED_DELETE_FROM_DB.format(name))
