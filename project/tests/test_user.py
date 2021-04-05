import pytest
from models import *

class TestUser(unittest.TestCase):
    def setUp(self):
        print("Setup")
    def test_new_user(new_user):
        """ Given User model, check when creating new user if all fields are correct """
        assert new_user.email == 'bucky_new@wisc.edu'
        assert new_user.username == 'wisc_user001'
        assert new_user.password != '*Bucky_W1ns!'
    def tearDown(self):
        print("Teardown")

if __name__ == "__main__":
    unittest.main(verbosity = 2)

