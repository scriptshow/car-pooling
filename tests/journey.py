import unittest
from app import app
import json


class JourneyTestCase(unittest.TestCase):
    """
    Tests cases for the Journey resource, including the DropOff.
    """

    def setUp(self):
        """
        Initializing values to be used in the test cases.
        """
        self.app = app
        self.client = self.app.test_client
        self.journey = {
            "id": 1,
            "people": 4
        }

    def test_journey_creation(self):
        """
        Test API can create a journey (POST request).
        """
        headers = {'Content-Type': 'application/json'}
        res = self.client().post('/journey', data=json.dumps(self.journey), headers=headers)
        self.assertEqual(200, res.status_code)

    def test_journey_deletion(self):
        """
        Test API can make a drop off for a journey (POST request).
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = self.client().post('/dropoff', data={'ID': self.journey['id']}, headers=headers)
        self.assertEqual(200, res.status_code)

    def tearDown(self):
        """
        Teardown all initialized variables.
        """
        # No TearDown needed
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
