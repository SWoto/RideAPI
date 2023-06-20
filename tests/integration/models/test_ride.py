from tests.base_test import RideBaseTest
from src.models import RideModel

FAILED_TO_FIND = "Did not find a this ride"
FAILED_DUPLICATED = "Duplicated this ride was previusly added to the database"
FAILED_SAVE_TO_DB = "Did not find ride after save_to_db"
FAILED_DELETE_FROM_DB = "Found ride after delete_from_db"


class RideTest(RideBaseTest):
    def test_save_to_db(self):
        ride = RideModel(**RideBaseTest.default_data_in)

        with self.app_context():
            ride.save_to_db()
            self.assertIsNotNone(RideModel.query.filter_by(
                id=ride.id).first(), FAILED_SAVE_TO_DB)

    def test_delete_from_db(self):
        ride = RideModel(**RideBaseTest.default_data_in)

        with self.app_context():
            ride.save_to_db()
            self.assertIsNotNone(RideModel.query.filter_by(
                id=ride.id).first(), FAILED_SAVE_TO_DB)

            ride.delete_from_db()
            self.assertIsNone(RideModel.query.filter_by(
                id=ride.id).first(), FAILED_DELETE_FROM_DB)

    def test_find_by_id(self):
        ride = RideModel(**RideBaseTest.default_data_in)

        with self.app_context():
            ride.save_to_db()
            self.assertIsNotNone(RideModel.find_by_id(ride.id), FAILED_TO_FIND)

    def test_crud(self):
        ride = RideModel(**RideBaseTest.default_data_in)

        with self.app_context():
            self.assertIsNone(RideModel.query.filter_by(
                id=ride.id).first(), FAILED_DUPLICATED)
            
            ride.save_to_db()

            self.assertIsNotNone(RideModel.query.filter_by(
                id=ride.id).first(), FAILED_SAVE_TO_DB)
            
            ride.delete_from_db()
            
            self.assertIsNone(RideModel.query.filter_by(
                id=ride.id).first(), FAILED_DELETE_FROM_DB)

    def test_find_rides_passenger(self):
        ride = RideModel(**RideBaseTest.default_data_in)

        with self.app_context():
            ride.save_to_db()
            found_passenger = RideModel.find_rides_passenger(ride.passenger_id)
            found_driver = RideModel.find_rides_passenger(ride.driver_id)
            self.assertEqual(1, len(found_passenger))
            self.assertEqual(ride, found_passenger[0])
            self.assertListEqual([], found_driver)

    def test_find_rides_driver(self):
        ride = RideModel(**RideBaseTest.default_data_in)

        with self.app_context():
            ride.save_to_db()
            found_passenger = RideModel.find_rides_driver(ride.passenger_id)
            found_driver = RideModel.find_rides_driver(ride.driver_id)
            self.assertEqual(1, len(found_driver))
            self.assertEqual(ride, found_driver[0])
            self.assertListEqual([], found_passenger)