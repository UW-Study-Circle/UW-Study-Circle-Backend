import pytest
from project.models import User
 
 
@pytest.fixture(scope='module')
def new_user():
    user = User("wisc_user001", "*Bucky_W1ns!", "bucky_new@wisc.edu", "Badger", "Bucky", 
    "Male", "123456789","28-01-1995")
    return user