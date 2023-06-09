import json

from tests.base_test import VehiclesBaseTest


class VehicleTest(VehiclesBaseTest):
    def test_register_vehicle(self):
        with self.app() as client:
            with self.app_context():
                data_out = VehicleTest.vehicle_data_out.copy()
                jwt = self.access_token
                request = client.post(
                    '/', json=VehicleTest.vehicle_data_in, headers={'Authorization': 'Bearer {}'.format(jwt)})
                result = json.loads(request.data)
                data_out['id'] = result['id']
                data_out['active'] = True

                self.assertDictEqual(data_out, result)

                request = client.post(
                    '/', json=VehicleTest.vehicle_data_in)

                self.assertEqual(request.status_code, 401)
                self.assertEqual(json.loads(request.text)[
                                 "msg"], "Missing Authorization Header")

    def test_register_duplicated_vehicle(self):
        with self.app() as client:
            with self.app_context():
                jwt = self.access_token
                client.post(
                    '/', json=VehicleTest.vehicle_data_in, headers={'Authorization': 'Bearer {}'.format(jwt)})

                request = client.post(
                    '/', json=VehicleTest.vehicle_data_in, headers={'Authorization': 'Bearer {}'.format(jwt)})

                self.assertEqual(request.status_code, 409)
                self.assertEqual(json.loads(request.text)[
                                 'message'], "A vehicle with that license plate already exists")

    def test_get_vehicle(self):
        with self.app() as client:
            with self.app_context():
                data_out = VehicleTest.vehicle_data_out.copy()

                request = client.post(
                    '/', json=VehicleTest.vehicle_data_in, headers={'Authorization': 'Bearer {}'.format(self.access_token)})

                result = json.loads(request.data)
                result_id = result['id']
                data_out['id'] = result_id
                data_out['active'] = True

                request = client.get("/{}".format(result_id))

                self.assertDictEqual(data_out, result)

    def test_get_all_vehicles(self):
        vehicles_cnt = 5
        data_in = VehicleTest.vehicle_data_in.copy()
        data_out = VehicleTest.vehicle_data_out.copy()
        data_in_multi = []
        data_out_multi = []
        for i in range(0, vehicles_cnt):
            data_tmp_in = data_in.copy()  
            data_tmp_in['license_plate'] = 'ABC0D1{}'.format(i)
            data_in_multi.append(data_tmp_in)

            data_tmp_out = data_out.copy()
            data_tmp_out['license_plate'] = data_tmp_in['license_plate']
            data_out_multi.append(data_tmp_out)

        with self.app() as client:
            with self.app_context():
                for i in range(0, vehicles_cnt):
                    request = client.post(
                        '/', json=data_in_multi[i], headers={'Authorization': 'Bearer {}'.format(self.access_token)})
                    data_out_multi[i]['id'] = json.loads(request.data)[
                        'id']
                    data_out_multi[i]['active'] = False if i < vehicles_cnt-1 else True

                request = client.get(
                    '/', headers={'Authorization': 'Bearer {}'.format(self.access_token)})

                self.assertListEqual(
                    data_out_multi, json.loads(request.data))

    def test_delete_vehicle(self):
        with self.app() as client:
            with self.app_context():
                request = client.post(
                    '/', json=VehicleTest.vehicle_data_in, headers={'Authorization': 'Bearer {}'.format(self.access_token)})

                result_id = json.loads(request.data)['id']
                request = client.delete("/{}".format(result_id))

                self.assertEqual(request.status_code, 401)
                self.assertEqual(json.loads(request.text)[
                                 "msg"], "Missing Authorization Header")

                request = client.delete("/{}".format(result_id), headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)})

                self.assertEqual(request.status_code, 200)
                self.assertEqual(json.loads(request.text)[
                                 'message'], "Vehicle deleted.")
