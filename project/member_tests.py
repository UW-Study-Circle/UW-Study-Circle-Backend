import unittest
import json
from server import app, db
import os
from flask.testing import FlaskClient


class GroupTestCase(unittest.TestCase):
    """This class represents the group test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_app(config_name="testing")
        # app.config['LOGIN_DISABLED'] = True
        self.client = app.test_client()
        app.config['TESTING'] = True
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

        
        

    def test_group_creation(self):
        """Test API can create a group (POST request)"""
        
        
        res = self.client.post('/api/group/',  headers={"Content-Type": "application/json"}, data=self.group)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group created", res.json['Success'])