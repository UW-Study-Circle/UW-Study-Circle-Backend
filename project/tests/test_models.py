from project.models import User, Group
'''Check of new user model creation and all fields are defined correctly'''
@pytest.fix
def test_new_user():
    user = User('test_email@wisc.edu', 'Test User', 'Wisc$User1!*')
    assert user.email == 'test_email@wisc.edu'
    assert user.password != 'Wisc$User1!*'
@pytest.fix
def test_new_group():
    group = Group('CSGroup1', 'Our group will be CSGroup1', 'CS506 Software Engineering', '30', '90', 'Private')
    assert group.groupname == 'CSGroup1'
    assert group.capacity <= 50 
    assert group.status == 'Private'
