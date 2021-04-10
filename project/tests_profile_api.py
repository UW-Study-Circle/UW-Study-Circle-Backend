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
<<<<<<< HEAD
        with app.app_context():
            # create all tables
            db.create_all()
        self.payload = json.dumps({
            "username": "wisc_user001", 
            "password": "*Bucky_W1ns!",
            "email": "bucky@wisc.edu",
            "lastname": "Badger",
            "firstname": "Bucky",
            "gender": "Male",
            "phonenumber": "123456789",
            "bday": "28-01-1995"
        })
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)

=======
>>>>>>> 794d8a521cebaf79625f5aa4abf2635516a1d87c
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
<<<<<<< HEAD
        response = self.client.get('/id/1', headers={"Content-Type": "application/json"})
        # print(response.json)
=======
        response = self.client.get('/id/10', headers={"Content-Type": "application/json"})
        # print(response.json)
        self.assertTrue(response.json['Message'] == "Successfully fetched user profile.")
>>>>>>> 794d8a521cebaf79625f5aa4abf2635516a1d87c
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
<<<<<<< HEAD
=======
        self.assertTrue(response.json['Message'] == "Sorry, couldn't fetch user profile.")
>>>>>>> 794d8a521cebaf79625f5aa4abf2635516a1d87c
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
<<<<<<< HEAD

=======
>>>>>>> 794d8a521cebaf79625f5aa4abf2635516a1d87c
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
<<<<<<< HEAD
        self.assertTrue(response.json["Success"] == "Login Successful")
=======
        self.assertTrue(response.json["Status"] == "Pass")
        self.assertTrue(response.json['Message'] == "User exists and correct credentials")
>>>>>>> 794d8a521cebaf79625f5aa4abf2635516a1d87c
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
<<<<<<< HEAD
        self.assertTrue(response.json["Content"] == None)
=======
        self.assertTrue(response.json["Status"] == "Fail")
        self.assertTrue(response.json['Message'] == "User does not exist or password is wrong.")
>>>>>>> 794d8a521cebaf79625f5aa4abf2635516a1d87c
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
<<<<<<< HEAD
    def test_put_reset_request_successful(self, **kwargs):
        """Test for putting successful reset request"""
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        payload = json.dumps({
            "cpwd":'*Bucky_W1ns!',
            "npwd":'*Bucky_W1ns!1',
            "cnpwd":'*Bucky_W1ns!1'
        })
        response = self.client.put('/api/profile/reset/', data= payload, content_type='application/json')
        print(response.json)
        self.assertTrue(response.json["Success"] == "New Password set successfully!")
        self.assertEqual(response.status_code, 200)
    def test_current_pass_not_equal_new_pass_unsuccessful(self, **kwargs):
        """Test for putting successful reset request"""
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        payload = json.dumps({
            "cpwd":'*Bucky_W1ns!',
            "npwd":'*Bucky_W1ns!',
            "cnpwd":'*Bucky_W1ns!1'
        })
        response = self.client.put('/api/profile/reset/', data= payload, content_type='application/json')
        print(response.json)
        self.assertTrue(response.json["Failure"] == "New Password and Current Password cannot be same. Try Again")
        self.assertEqual(response.status_code, 200)
    def test_put_reset_newpass_not_equal_confirm_unsuccessful(self, **kwargs):
        """Test for putting successful reset request"""
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        payload = json.dumps({
            "cpwd":'*Bucky_W1ns!',
            "npwd":'*Bucky_W1ns!1',
            "cnpwd":'*Bucky_W1ns!2'

        })
        response = self.client.put('/api/profile/reset/', data= payload, content_type='application/json')
        print(response.json)
        self.assertTrue(response.json["Failure"] == "New Password and Confirm New password does not match. Try Again")
        self.assertEqual(response.status_code, 200)
    def test_user_reset_with_incorrect_json(self):
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        res = self.client.put('/api/profile/reset/',  headers={"Content-Type": "text/plain"}, data="1234")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Data not in correct format", res.json['Error'])
    def test_user_reset_with_none_json(self):
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        res = self.client.put('/api/profile/reset/',  headers={"Content-Type": "text/plain"}, data=None)
        print(res.json)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Data not in correct format", res.json['Error'])
    def test_post_login_with_none_or_incorrect_json(self):
        
        res = self.client.post('/api/login/',  headers={"Content-Type": "text/plain"}, data="1234")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Data not in correct format", res.json['Error'])
    def tearDown(self):
        "Tear down Profile API test fixtures"
        print('### Tearing down the flask server ###')
        with app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
=======

    def tearDown(self):
        "Tear down Profile API test fixtures"
        print('### Tearing down the flask server ###')
>>>>>>> 794d8a521cebaf79625f5aa4abf2635516a1d87c
if __name__ == "__main__":
        unittest.main(verbosity = 2)