import pytest
from test.factories.user.factories import UserFactory, UserTwoFactory, UserThreeFactory
from test.factories.user.factories import TeamFactory
from django.test import Client
from rest_framework.test import APIClient


from django.core.management import call_command

@pytest.fixture(autouse=True)
def clear_db():
    call_command('flush', '--noinput')
    
    
@pytest.fixture(autouse=True)
def create_team():
    return TeamFactory.create()


@pytest.fixture
def user_creation_one(): 
    return UserFactory.create()

@pytest.fixture
def user_creation_two(): 
    return UserTwoFactory.create()


@pytest.fixture
def user_creation_three(): 
    return UserThreeFactory.create()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def authenticated_client(client, user_creation_one):
    user = user_creation_one
    client.force_authenticate(user=user)
    return client
    
    
    