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
        with app.app_context():
            # create all tables
            db.create_all()
        

        
        self.group =  json.dumps({
                "groupname" : "cs506",
                "courseinfo": "cs506",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"this is a group",
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

        
        

    def test_group_creation(self):
        """Test API can create a group (POST request)"""
        
        
        res = self.client.post('/api/group/',  headers={"Content-Type": "application/json"}, data=self.group)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group created", res.json['Success'])

    def test_same_groupname_creation(self):
        """Test API create a duplicate group (POST request)"""
        
        res = self.client.post('/api/group/',headers={"Content-Type": "application/json"},  data=self.group)
        
        group2 = json.dumps({
                "groupname" : "cs506",
                "courseinfo": "cs506",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"this is a group",
                "status" : "public"
        })
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=group2)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group Name already exists", res.json['Duplicate'])
        
    
    def test_access_empty_group(self):
        """Test API  with no group (GET request)"""
        
        res = self.client.get('/api/group/', headers={"Content-Type": "application/json"})
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json['Content'])
        
    def test_api_can_get_groups(self):
        """Test API can get a group (GET request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        group2 = json.dumps({
                "groupname" : "cs536",
                "courseinfo": "cs536",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"this is a group",
                "status" : "public"
        })
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=group2)
        
        res = self.client.get('/api/group/', headers={"Content-Type": "application/json"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(2, len(res.json['Content']))


    def test_group_deletion(self):
        """Test API can delete an existing group. (DELETE request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        group2 = json.dumps({
                "groupname" : "cs536",
                "courseinfo": "cs536",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"this is a group",
                "status" : "public"
        })
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=group2)
        
        rm = self.client.delete('/api/group/id/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group deleted", rm.json['Success'])
        
        # Test to see if it exists, should return a 405
        
        res = self.client.get('/api/group/', headers={"Content-Type": "application/json"})
        self.assertEqual(res.status_code, 200)
        print("aaaaaaaaaaaaaaaaa", res.json)
        # self.assertEqual(1, len(res.json['Content']))
        
    
        
    def test_nonexise_group_deletion(self):
        """Test API can delete an none existing group. (DELETE request)."""
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=self.group)
        
        group2 = json.dumps({
                "groupname" : "cs536",
                "courseinfo": "cs536",
                "capacity": 50,
                "duration": 100000,
                "level": "3",
                "description":"this is a group",
                "status" : "public"
        })
        res = self.client.post('/api/group/', headers={"Content-Type": "application/json"}, data=group2)
        
        rm = self.client.delete('/api/group/id/3')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group not found", rm.json['Content'])
        

    def tearDown(self):
        """teardown all initialized variables."""
        with app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
