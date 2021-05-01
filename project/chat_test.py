import unittest
import json
from server import app, db
from populate_data import *





class ChatTestCase(unittest.TestCase):
    """This class represents the member test case"""

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
        res = self.client.post('/chat', query_string={'groupid': 1})
        print(res.status_code, res.json)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json, None)
        
    
    def test_post_message_with_a_group_id(self):

        res = self.client.post('/chat', query_string={'groupid': 2})
        # print(response.status_code, response.json)
        self.assertEqual(res.status_code, 200)
        res = self.client.get('/chat')
        with self.client.session_transaction() as session:
            try:
                self.assertEqual(session['room'], 'Assembly Language Group')
                self.assertEqual(session['name'], 'akshat')
                self.assertEqual(session['user_id'], 1)
                self.assertEqual(session['group_id'], '2')
            except KeyError:
                raise AssertionError('nothing flashed')
      
        
    def test_post_message_in_unvalid_group(self):
        
        response = self.client.post('/chat', query_string={'groupid': 10})
        response = self.client.get('/chat')
        # assert "_flashes" in session
        with self.client.session_transaction() as session:
            try:
                print(session)
                category, message = session['_flashes'][0]
            except KeyError:
                raise AssertionError('nothing flashed')
            assert "Group not found" in message
            self.assertEqual(category, 'message')
            
            
    def test_post_message_not_a_member(self):
   
        response = self.client.post('/chat', query_string={'groupid': 4})
        print(response)
        response = self.client.get('/chat')
        # assert "_flashes" in session
        with self.client.session_transaction() as session:
            try:
                print(session)
                category, message = session['_flashes'][0]
            except KeyError:
                raise AssertionError('nothing flashed')
            assert "Member not existed." in message
            self.assertEqual(category, 'message')
    
    
    def tearDown(self):
        """teardown all initialized variables."""
        with app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()