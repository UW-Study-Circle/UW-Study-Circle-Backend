import unittest
import json

from app import app
from database.db import db


import os
import json
from app import create_app, db


class GroupTestCase(unittest.TestCase):
    """This class represents the group test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.group =  json.dumps({
                "groupname" : "cs506",
                "courseinfo": "cs506",
                "capacity": 50,
                "duration": "100000",
                "level": 3,
                "description":"this is a group",
                "status" : "public",
        })

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_group_creation(self):
        """Test API can create a group (POST request)"""
        res = self.client().post('/api/group/', data=self.group)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group created", res.json['Success'])

    def test_api_can_get_group(self):
        """Test API can get a group (GET request)."""
        res = self.client().post('/api/group/', data=self.group)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/group/groupname/cs506')
        self.assertEqual(res.status_code, 200)
        
        self.assertIn(self.group, res.json["Content"])   #???????????????


    def test_group_deletion(self):
        """Test API can delete an existing group. (DELETE request)."""
        rv = self.client().post(
            '/bucketlists/',
            data=self.group)
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/api/group/id/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/group/id/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
