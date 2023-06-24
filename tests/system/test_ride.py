import json
import uuid

from tests.base_test import RideBaseTest
from src.models import RideModel, VehicleModel


class RideTest(RideBaseTest):

    def test_resgister_ride(self):
        data_in = RideTest.default_data_in_system.copy()

        with self.app() as client:
            with self.app_context():
                jwt = self.access_token

                request = client.post(
                    '/', json=data_in, headers={'Authorization': 'Bearer {}'.format(jwt)})

                received = json.loads(request.data)
                received.pop('id')

                self.assertEqual(request.status_code, 201)
                self.assertDictEqual(RideBaseTest.default_data_out, received)

    def test_resgister_ride_no_auth(self):
        data_in = RideTest.default_data_in.copy()

        with self.app() as client:
            with self.app_context():
                request = client.post('/', json=data_in)
                
                self.assertEqual(request.status_code, 401)
                self.assertEqual(json.loads(request.data), {
                                 'msg': 'Missing Authorization Header'})
