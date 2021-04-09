import unittest
import json
from server import db, app


class MemberAPITest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MemberAPITest, self).__init__(*args, **kwargs)
        self.client = app.test_client()
    def setUp(self):
        "Set up Member API test fixtures"
        print('### Setting up flask server ###')
    
    def test_get_grouplist_successful_authenticated(self):
        """ Test to get the group list for user id """
        response = self.client.get('/api/member/groups/5', content_type='application/json')
        self.assertEqual(response.status_code, 200)



    def tearDown(self):
        "Tear down Member API test fixtures"
        print('### Tearing down the flask server ###')
if __name__ == "__main__":
        unittest.main(verbosity = 2)