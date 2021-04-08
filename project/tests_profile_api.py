# user_tests 
import unittest
import json
from server import db, app


class ProfileAPITest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ProfileAPITest, self).__init__(*args, **kwargs)
        self.client = app.test_client()
    def setUp(self):
        "Set up Profile API test fixtures"
        print('### Setting up flask server ###')
    def test_successful_get_user_profile_by_id(self):
        """Test getting the logged-in user's profile"""
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        response = self.client.get('/id/10', headers={"Content-Type": "application/json"})
        # print(response.json)
        self.assertTrue(response.json['Message'] == "Successfully fetched user profile.")
        self.assertTrue(response.json['username'] == "wisc_user001")
        self.assertTrue(response.json['firstname'] == "Bucky")
        self.assertTrue(response.json['lastname'] == "Badger")
        self.assertEqual(response.status_code, 200)
    def test_invalid_id_get_user_profile(self):
        """Test getting the logged-in user's profile"""
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        response = self.client.get('/id/null', headers={"Content-Type": "application/json"})
        # print(response.json)
        self.assertTrue(response.json['Message'] == "Sorry, couldn't fetch user profile.")
        self.assertTrue(response.json['username'] == None)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/id/''', headers={"Content-Type": "application/json"})
        # print(response.json)
        self.assertTrue(response.json == None)
        self.assertEqual(response.status_code, 404)

    def test_successful_logout_user(self):
        """Test logging out user feature"""
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        # print(response.json)
        response = self.client.get('/api/logout/true',content_type='application/json')
        self.assertIn(b'Logout Successful!', response.data)
        self.assertEqual(response.status_code, 200)
    def test_registered_successful_login(self):
        """ Test for login of non-registered user """
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        # print(response.json)
        self.assertTrue(response.json["Status"] == "Pass")
        self.assertTrue(response.json['Message'] == "User exists and correct credentials")
        self.assertEqual(response.status_code, 200)


    def test_non_registered_unsuccessful_login(self):
        """ Test for login of non-registered user """
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='joe@gmail.com',
                password='123456'
            )),
            content_type='application/json'
        )
        self.assertTrue(response.json["Status"] == "Fail")
        self.assertTrue(response.json['Message'] == "User does not exist or password is wrong.")
        self.assertEqual(response.status_code, 200)

    def test_get_profile_unauthenticated(self):
        """ Test for login of non-registered user """
        response = self.client.get('/', content_type='application/json')
        self.assertTrue(response.json["Error"] == "Unauthenticated")
        self.assertEqual(response.status_code, 200)

    def test_get_profile_authenticated(self):
        """ Test for login of non-registered user """
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        response = self.client.get('/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        "Tear down Profile API test fixtures"
        print('### Tearing down the flask server ###')
if __name__ == "__main__":
        unittest.main(verbosity = 2)