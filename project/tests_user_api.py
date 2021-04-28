# user_tests 
import unittest
import json
from server import db, app


class UserAPITest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UserAPITest, self).__init__(*args, **kwargs)
        self.client = app.test_client()
    def setUp(self):
        "Set up User API test fixtures"
        print('### Setting up flask server ###')
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

    def test_successful_signup(self):
        # When
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        print(response.json)
        # Then
        self.assertTrue(response.json['Success'] == "New user has been successfully created")
        self.assertEqual(response.status_code, 200)
        
    def test_duplicate_username_signup(self):
        payload1 = json.dumps({
                "username": "wisc_user001", 
                "password": "*Bucky_W1ns!",
                "email": "bucky_new@wisc.edu",
                "lastname": "Badger",
                "firstname": "Bucky",
                "gender": "Male",
                "phonenumber": "123456789",
                "bday": "28-01-1995"
        })

        # When
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=payload1)
        print(response.json)
        # Then
        self.assertTrue(response.json['Duplicate'] == "Username already exists")
        self.assertEqual(response.status_code, 200)
    
    def test_duplicate_email_signup(self):
        payload2 = json.dumps({
                "username": "wisc_user002", 
                "password": "*Bucky_W1ns!",
                "email": "bucky@wisc.edu",
                "lastname": "Badger",
                "firstname": "Bucky",
                "gender": "Male",
                "phonenumber": "123456789",
                "bday": "28-01-1995"
        })
        # When
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=payload2)
        # Then
        self.assertTrue(response.json['Duplicate'] == "Email already exists")
        self.assertEqual(response.status_code, 200)
    def test_successful_delete_user(self):
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        # User needs to be logged in
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        # When user exists
        response = self.client.delete('/api/user/id/1', headers={"Content-Type": "application/json"})
        # Then
        self.assertTrue(response.json['Success'] == "User has been successfully deleted")
        self.assertEqual(200, response.status_code)

    def test_unsuccessful_delete_user(self):
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        # User needs to be logged in
        response = self.client.post(
            '/api/login/',
            data=json.dumps(dict(
                email='bucky@wisc.edu',
                password='*Bucky_W1ns!'
            )),
            content_type='application/json'
        )
        
        payload2 = json.dumps({
            "username": "wisc_user002", 
            "password": "*Bucky_W1ns!",
            "email": "bucky2@wisc.edu",
            "lastname": "Badger",
            "firstname": "Bucky",
            "gender": "Male",
            "phonenumber": "123456789",
            "bday": "28-01-1995"
        })
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=payload2)
        response = self.client.delete('/api/user/id/2', headers={"Content-Type": "application/json"})
        self.assertTrue(response.json['Error'] == "Incorrect User ID")
        # Then
        self.assertEqual(200, response.status_code)
        
        
        # When logged in user tries to delete user doesn't exist
        response = self.client.delete('/api/user/id/3', headers={"Content-Type": "application/json"})
        # Then
        self.assertTrue(response.json['Content'] == "User not found")
        self.assertEqual(200, response.status_code)

        # When passing invalid input like null
        response = self.client.delete('/api/user/id/null', headers={"Content-Type": "application/json"})
        self.assertTrue(response.json['Error'] == "Incorrect or Null ID")
        # Then
        self.assertEqual(200, response.status_code)

        # When passing invalid input like null
        response = self.client.delete('/api/user/id/''', headers={"Content-Type": "application/json"})
        # Then
        print(response.json)
        self.assertTrue(response.json == None)
        self.assertEqual(404, response.status_code)
        
        
        
        
        
        
    def test_successful_search_user(self):
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        response = self.client.get('/api/user/email/bucky@wisc.edu/password/*Bucky_W1ns!', headers={"Content-Type": "application/json"})
        # Then
        self.assertTrue(response.json['Success'] == "Success searching for user")
        self.assertEqual(200, response.status_code)
    def test_unsuccessful_search_user(self):
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        response = self.client.get('/api/user/email/invalid@wisc.edu/password/*Bucky_W1ns!', headers={"Content-Type": "application/json"})
        # Then
        self.assertTrue(response.json['Content'] == None)
        self.assertEqual(200, response.status_code)
    def test_invalid_inputs_search_user(self):
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)
        response = self.client.get('/api/user/email/''/password/pass', headers={"Content-Type": "application/json"})
        print(response.json)
        # Then
        self.assertTrue(response.json == None)
        self.assertEqual(404, response.status_code)
        
        
    def test_user_creation_with_none_json(self):
        
        res = self.client.post('/api/user/',  headers={"Content-Type": "text/plain"}, data="1234")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Data not in correct format", res.json['Error'])

    def tearDown(self):
        "Tear down User API test fixtures"
        print('### Tearing down the flask server ###')
        with app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
        unittest.main(verbosity = 2)