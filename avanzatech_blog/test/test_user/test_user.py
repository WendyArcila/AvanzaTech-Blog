import pytest 




@pytest.mark.django_db
def test_common_user_creation(user_creation_one):
    assert user_creation_one.is_staff == False
    
'''
@pytest.mark.django_db    
def test_superuser_creation_one(user_creation_one):
    user_creation_one.is_superuser == True
    user_creation_one.is_staff == True 
    assert user_creation_one.is_superuser 
    '''

@pytest.mark.django_db    
def test_staff_user_creation_one(user_creation_one):
    user_creation_one.is_staff = True
    assert user_creation_one.is_staff
    
''' 
@pytest.mark.django_db   
def test_user_creation_one_fail():
    with pytest.raises(Exception):
   '''     