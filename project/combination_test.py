# user_tests 
import unittest
import json
from server import db, app
from populate_data import * 

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
        # When logged in user tries to delete user doesn't exist
        response = self.client.delete('/api/user/id/2', headers={"Content-Type": "application/json"})
        # Then
        self.assertTrue(response.json['Error'] == "Incorrect User ID")
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


class ProfileAPITest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ProfileAPITest, self).__init__(*args, **kwargs)
        self.client = app.test_client()
    def setUp(self):
        "Set up Profile API test fixtures"
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
        response = self.client.post('/api/user/', headers={"Content-Type": "application/json"}, data=self.payload)

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
        response = self.client.get('/id/1', headers={"Content-Type": "application/json"})
        # print(response.json)
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
        self.assertTrue(response.json["Success"] == "Login Successful")
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
        self.assertTrue(response.json["Content"] == None)
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
        print("aaaaaaaaaaaaaaaaaaaaa",res.json)
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

if __name__ == "__main__":
        unittest.main(verbosity = 2)