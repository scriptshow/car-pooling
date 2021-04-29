import unittest
from app import app


class StatusTestCase(unittest.TestCase):
    """
    Tests cases for the Cabify status resource.
    """

    def setUp(self):
        """
        Initializing values to be used in the test cases.
        """
        self.app = app
        self.client = self.app.test_client

    def test_status(self):
        """
        Test API status resource (GET request).
        """
        res = self.client().get('/status')
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
