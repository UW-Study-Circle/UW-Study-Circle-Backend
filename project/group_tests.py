import unittest
import json
from server import app, db
import os
from flask.testing import FlaskClient
import requests
from sqlalchemy_utils import database_exists
from flask_login import login_user, logout_user, login_required, current_user
# from populate_data import *
# from app import create_app, db
import base64
from models import User, Group

class GroupTestCase(unittest.TestCase):
    """This class represents the group test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_app(config_name="testing")
        # app.config['LOGIN_DISABLED'] = True
        self.client = app.test_client()
        # app.config['TESTING'] = True
        with app.app_context():
            # create all tables
            db.create_all()
        

        
        self.group =  json.dumps({
                "groupname" : "cs506",
                "courseinfo": "Software Enigneering",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"Software Engineering is a course that closely resembles the real-world. Over the course of the semester I will serve as your pilot on a 30,000 ft above sea-level tour of most things software engineering. I will take a breadth-first approach to covering the software engineering process from requirements gathering to project completion.",
                "status" : "public"
        })
        
        self.group2 = json.dumps({
                "groupname" : "cs536",
                "courseinfo": "Introduction to Programming Languages and Compilers",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"Introduction to the theory and practice of compiler design. Comparison of features of several programming languages and their implications for implementation techniques. Several programming projects required.",
                "status" : "public"
        })
        
        self.new_user = json.dumps({
                "username": "wisc_user001", 
                "password": "*Bucky_W1ns!",
                "email": "bucky_diff@wisc.edu",
                "lastname": "Badger",
                "firstname": "Bucky",
                "gender": "Male",
                "phonenumber": "123456789",
                "bday": "28-01-1995"
        })
        
        self.login_user = json.dumps({
                "email": "bucky_diff@wisc.edu",
                "password": "*Bucky_W1ns!"
                
        })
        
        
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.new_user)
        
        response = self.client.post('/api/login/' , headers={"Content-Type": "application/json"}, data=self.login_user)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Set-Cookie'])

        
        
    def test_auth(self):
        """Test API can't be accessible withou authority."""
        
        logout = self.client.get('/api/logout/True')
        res = self.client.post('/api/group/',  headers={"Content-Type": "application/json"}, data=self.group)
        # print("gggggggggggggggggggggggggg", res, res.status_code)
        self.assertEqual(res.status_code, 401)
        
        res2 = self.client.get('/api/group/')
        self.assertEqual(res2.status_code, 401)
        
        res3 = self.client.delete('/api/group/id/1')
        self.assertEqual(res3.status_code, 401)
        
    def test_group_creation(self):
        """Test API can create a group (POST request)"""
        
        
        res = self.client.post('/api/group/',  headers={"Content-Type": "application/json"}, data=self.group)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group created", res.json['Success'])
        
    def test_group_creation_with_none_json(self):
        
        res = self.client.post('/api/group/',  headers={"Content-Type": "text/plain"}, data="1234")
       
        self.assertEqual(res.status_code, 200)
        # print("eeeeeeeeeeeeeeeeeeeeeee", res.json)
        self.assertIn("Data not in correct format", res.json['Error'])

    def test_same_groupname_creation(self):
        """Test API create a duplicate group (POST request)"""
        
        res = self.client.post('/api/group/',headers={"Content-Type": "application/json"},  data=self.group)
        
        group2 =  json.dumps({
                "groupname" : "cs506",
                "courseinfo": "Software Enigneering",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"Software Engineering is a course that closely resembles the real-world. Over the course of the semester I will serve as your pilot on a 30,000 ft above sea-level tour of most things software engineering. I will take a breadth-first approach to covering the software engineering process from requirements gathering to project completion.",
                "status" : "public"
        })
        
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=group2)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group Name already exists", res.json['Duplicate'])
        
    
    def test_access_empty_group(self):
        """Test API  with no group (GET request)"""
        
        res = self.client.get('/api/group/', headers={"Content-Type": "application/json"})
        print("ffffffffffffffffffffffffffffff", res.json)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json['Content'])
       
        
    def test_api_can_get_groups(self):
        """Test API can get all groups (GET request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
       
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        res = self.client.get('/api/group/', headers={"Content-Type": "application/json"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(2, len(res.json['Content']))
        
    def test_api_can_get_group_by_id(self):
        """Test API can get a group by id(GET request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        res = self.client.get('/api/group/id/2')
        
        self.assertEqual(res.status_code, 200)
        # print("cccccccccccccccccccccccccccccccc", res.json)
        self.assertEqual("cs536", res.json['groupname'])
        
    def test_api_can_get_group_by_nonexisting_id(self):
        """Test API can get a group by nonexisting id(GET request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        res = self.client.get('/api/group/id/3')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual("{}", str(res.json))

    def test_api_can_get_group_by_search(self):
        """Test API can get a group by search(GET request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
    
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        res = self.client.get('/api/group/engineering')
        # print("bbbbbbbbbbbbbbbbbbbbbbbbb", res.json['Content'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual("cs506", res.json['Content'][0]['groupname'])
    
    def test_api_group_search_result_is_empty(self):
        
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        res = self.client.get('/api/group/python')
        
        self.assertEqual(res.status_code, 200)
        # print("cccccccccccccccccccccccccccccccc", res.json)
        self.assertEqual(0, len(res.json['Content']))

    def test_group_deletion(self):
        """Test API can delete an existing group. (DELETE request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
       
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        rm = self.client.delete('/api/group/id/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group deleted", rm.json['Success'])
        
        # Test to see if it exists, should return a 405
        
        res = self.client.get('/api/group/')
        self.assertEqual(res.status_code, 200)
        # print("dddddddddddddddddddddddddddddddddd", res.json)
        self.assertEqual(1, len(res.json['Content']))
        
    
        
    def test_nonexise_group_deletion(self):
        """Test API can delete an none existing group. (DELETE request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        rm = self.client.delete('/api/group/id/3')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group not found", rm.json['Content'])

    def test_deletion_by_not_admin(self):
        """Test API deleted by a none admin user. (DELETE request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group2)
        
        logout = self.client.get('/api/logout/True')
        user2 = json.dumps({
                "username": "wisc_user002", 
                "password": "*Bucky_W1ns!",
                "email": "bucky_diff2@wisc.edu",
                "lastname": "Badger",
                "firstname": "Bucky",
                "gender": "Male",
                "phonenumber": "123456789",
                "bday": "28-01-1995"
        })
        
        login_user2 = json.dumps({
                "email": "bucky_diff2@wisc.edu",
                "password": "*Bucky_W1ns!"
                
        })
        
        
        response2 = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=user2)
        
        response2 = self.client.post('/api/login/' , headers={"Content-Type": "application/json"}, data=login_user2)
        
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.headers['Set-Cookie'])
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", response2.headers)
        
        rm = self.client.delete('/api/group/id/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Not admin", rm.json['Error'])
        
        

    def tearDown(self):
        """teardown all initialized variables."""
        with app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
