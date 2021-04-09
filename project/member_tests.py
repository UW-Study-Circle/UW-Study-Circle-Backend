import unittest
import json
from server import app, db
import os
from flask.testing import FlaskClient
from populate_data import *


class MemberTestCase(unittest.TestCase):
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
        

        populate_data()
        
        self.login_user = json.dumps({
                "email": "a@e.c",
                "password": "aaaa"
                
        })
        
        response = self.client.post('/api/login/' , headers={"Content-Type": "application/json"}, data=self.login_user)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Set-Cookie'])

        
    def test_auth(self):
        """Test API can't be accessible withou authority."""
        
        logout = self.client.get('/api/logout/True')
        
        res = self.client.get('/api/member/groups/2')
      
        self.assertEqual(res.status_code, 401)
        
        res2 = self.client.get('/api/member/members/1')
        self.assertEqual(res2.status_code, 401)
        
        member = json.dumps({
                "group_id": 3,
                "request_id": 1,
                "approval": False
        })
        
        res3 = self.client.post('/api/member/request/',  headers={"Content-Type": "application/json"}, data=member)
        self.assertEqual(res3.status_code, 401) 
        
        res4 = self.client.put('/api/member/join/1')  
        self.assertEqual(res4.status_code, 401) 
         

    def test_get_groups_without_auth(self):
        """Test API can't access group info by other users"""
        
        
        res = self.client.get('/api/member/groups/2')
        
        self.assertEqual(res.status_code, 200)
        self.assertIn("Unauthorized request", res.json['Error'])
        
    def test_get_members_with_group_id(self):
        """Test API can access members by group id"""

        res = self.client.get('/api/member/members/1')
        
        self.assertEqual(res.status_code, 200)
       
        self.assertEqual(4, res.json[0]['user_id'])
        self.assertEqual(1, res.json[1]['user_id'])
        
    def test_get_members_with_notexisting_group_id(self):
        
        """Test API can access members by wrong group id"""
        res = self.client.get('/api/member/members/8')
        self.assertEqual(res.status_code, 200)
       
        self.assertEqual("[]", str(res.json))
        
#     def test_get_groups_without_user_id(self):
#         """Test API can access group info without user id"""
 
#         res = self.client.get('/api/member/groups')
        
#         self.assertEqual(res.status_code, 404)
       
#         print("zzzzzzzzzzzzzzzzzzzzzzzz", res.json)
#         self.assertEqual(1, res.json[0][id])
#         self.assertEqual(4, res.json[1][id])

    def test_get_groups_by_user_id(self):
        """Test API can access group info by logged user"""
 
        res = self.client.get('/api/member/groups/1')
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(1, res.json[0]['group_id'])
        self.assertEqual(2, res.json[1]['group_id'])
        
    def test_group_creation_with_none_json(self):
        
        res = self.client.post('/api/member/request/',  headers={"Content-Type": "text/plain"}, data="1234")
       
        self.assertEqual(res.status_code, 200)
        self.assertIn("Data not in correct format", res.json['Error'])
        
    def test_member_request_with_none_existing_group(self):
        
        member = json.dumps({
                "group_id": 5,
                "request_id": 1,
                "approval": False
            })
        
        res = self.client.post('/api/member/request/',  headers={"Content-Type": "application/json"}, data=member)
       
        self.assertEqual(res.status_code, 200)
        self.assertIn("Group not found", res.json['Error'])
        
    def test_member_request_with_wrong_admin_id(self):
        member = json.dumps({
                "group_id": 3,
                "request_id": 1,
                "approval": False
        })
        
        res = self.client.post('/api/member/request/',  headers={"Content-Type": "application/json"}, data=member)
       
        self.assertEqual(res.status_code, 200)
        self.assertIn("Unauthorized request", res.json['Error'])

    def test_member_request_with_wrong_request_id(self):
        member = json.dumps({
                "group_id": 1,
                "request_id": 10,
                "approval": False
        })
        
        res = self.client.post('/api/member/request/',  headers={"Content-Type": "application/json"}, data=member)
       
        self.assertEqual(res.status_code, 200)
        self.assertIn("Request not found", res.json['Error'])
        
    def test_member_request_with__private_group_and_approved(self):
        member = json.dumps({
                "group_id": 1,
                "request_id": 4,
                "approval": True
        })
        
        res = self.client.post('/api/member/request/',  headers={"Content-Type": "application/json"}, data=member)
       
        self.assertEqual(res.status_code, 200)
        # print("eeeeeeeeeeeeeeeeeeeeeee", res.json)
        self.assertIn("Request Approved", res.json['Status'])

    def test_member_request_with_private_group_and_not_approved(self):
        member = json.dumps({
                "group_id": 1,
                "request_id": 4,
                "approval": False
        })
        
        res = self.client.post('/api/member/request/',  headers={"Content-Type": "application/json"}, data=member)
       
        self.assertEqual(res.status_code, 200)
       
        self.assertIn("Request Denied", res.json['Status'])
        
    def test_member_request_with_public_group(self):
        member = json.dumps({
                "group_id": 1,
                "request_id": 5,
                "approval": False
        })
        
        res = self.client.post('/api/member/request/',  headers={"Content-Type": "application/json"}, data=member)
       
        self.assertEqual(res.status_code, 200)
        
        self.assertIn("No change in request", res.json['Status'])

    def test_put_members_into_joined_group(self):
        """Test API can access members by group id"""

        res = self.client.put('/api/member/join/1')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual("Member already Exists", res.json['Error'])
        
    def test_put_members_with_notexisting_group_id(self):
        
        """Test API can access members by wrong group id"""
        res = self.client.put('/api/member/join/8')
        self.assertEqual(res.status_code, 200)
      
        self.assertEqual("Group does not exist", res.json['Error'])
        
    def test_put_members_into_public_group(self):
        """Test API can access members by group id"""

        res = self.client.put('/api/member/join/4')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual("Member Added", res.json['Success'])
        
    def test_put_members_into_private_group(self):
        """Test API can access members by group id"""

        res = self.client.put('/api/member/join/3')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual("Member's Request Added. Waiting for Admin Approval", res.json['Success'])
           
    def tearDown(self): 
        """teardown all initialized variables."""
        with app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()