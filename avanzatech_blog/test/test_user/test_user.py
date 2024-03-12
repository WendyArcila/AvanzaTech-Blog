import pytest 





@pytest.mark.django_db
def test_common_user_creation(user_creation):
    assert user_creation.is_staff == False
    
'''
@pytest.mark.django_db    
def test_superuser_creation(user_creation):
    user_creation.is_superuser == True
    user_creation.is_staff == True 
    assert user_creation.is_superuser 
    '''

@pytest.mark.django_db    
def test_staff_user_creation(user_creation):
    user_creation.is_staff = True
    assert user_creation.is_staff
    
''' 
@pytest.mark.django_db   
def test_user_creation_fail():
    with pytest.raises(Exception):
   '''     