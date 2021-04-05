# user_tests 
import unittest
import json
from server import db, app


class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()
    
    def test_successful_signup(self):
        # Given
        payload = json.dumps({
                "username": "wisc_user001", 
                "password": "*Bucky_W1ns!",
                "email": "bucky@wisc.edu",
                "lastname": "Badger",
                "firstname": "Bucky",
                "gender": "Male",
                "phonenumber": "123456789",
                "bday": "28-01-1995"
        })

        # When
        response = self.app.post('/api/user/', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)
    def test_duplicate_username_signup(self):
        payload = json.dumps({
                "username": "wisc_user001", 
                "password": "*Bucky_W1ns!",
                "email": "bucky_diff@wisc.edu",
                "lastname": "Badger",
                "firstname": "Bucky",
                "gender": "Male",
                "phonenumber": "123456789",
                "bday": "28-01-1995"
        })

        # When
        response = self.app.post('/api/user/', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['Duplicate']))
        self.assertEqual(400, response.status_code)
    
    def test_duplicate_email_signup(self):
        payload = json.dumps({
                "username": "wisc_user001", 
                "password": "*Bucky_W1ns!",
                "email": "bucky@wisc.edu",
                "lastname": "Badger",
                "firstname": "Bucky",
                "gender": "Male",
                "phonenumber": "123456789",
                "bday": "28-01-1995"
        })

        # When
        response = self.app.post('/api/user/', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['Duplicate']))
        self.assertEqual(400, response.status_code)

    def test_successful_delete_user(self):

        # When user exists
        response = self.app.delete('/api/user/id/<id>', data={'id','id'}, headers={"Content-Type": "application/json"})

        # Then
        self.assertEqual(str, type(response.json['Success']))
        self.assertEqual(200, response.status_code)

    def test_unsuccessful_delete_user(self):

        # When user doesn't exist
        response = self.app.delete('/api/user/id/<id>', data={'id','id'}, headers={"Content-Type": "application/json"})

        # Then
        self.assertEqual(str, type(response.json['Content']))
        self.assertEqual(400, response.status_code)

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)
            
    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1')
        self.assertIn('Dont just eat', str(results.data))