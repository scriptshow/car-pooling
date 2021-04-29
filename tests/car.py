import unittest
from app import app
from shared.config import MIN_CAR_SEATS, MAX_CAR_SEATS
from random import randint
import json


class CarTestCase(unittest.TestCase):
    """
    Tests cases for the Cabify cars resource.
    """

    def setUp(self):
        """
        Initializing values to be used in the test cases.
        """
        self.app = app
        self.client = self.app.test_client
        self.car_list = []
        for x in range(1, 100000):
            self.car_list.append({
                'id': x,
                'seats': randint(MIN_CAR_SEATS, MAX_CAR_SEATS)
            })
        self.car_id_failure = [{
            'id': '1',
            'seats': randint(MIN_CAR_SEATS, MAX_CAR_SEATS)
        }]
        self.car_seats_failure = [{
            'id': 1,
            'seats': 2
        }]
        self.car_malformed_failure = [{
            'id': 1,
        }]
        self.car_duplicate_failure = [{
            'id': 1,
            'seats': randint(MIN_CAR_SEATS, MAX_CAR_SEATS)
        }, {
            'id': 1,
            'seats': randint(MIN_CAR_SEATS, MAX_CAR_SEATS)
        }]
        self.failures_list = [self.car_id_failure, self.car_seats_failure, self.car_malformed_failure, self.car_duplicate_failure]


    def test_car_list_creation(self):
        """
        Test API can create a list of cars (PUT request).
        """
        headers = {'Content-Type': 'application/json'}
        res = self.client().put('/cars', data=json.dumps(self.car_list), headers=headers)
        self.assertEqual(200, res.status_code)

    def test_car_failure_creation(self):
        """
        Test API failure when input data is not correct (PUT request).
        """
        headers = {'Content-Type': 'application/json'}
        for failure_set in self.failures_list:
            res = self.client().put('/cars', data=json.dumps(failure_set), headers=headers)
            self.assertEqual(400, res.status_code)

    def tearDown(self):
        """
        Teardown all initialized variables.
        """
        # No TearDown needed
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
