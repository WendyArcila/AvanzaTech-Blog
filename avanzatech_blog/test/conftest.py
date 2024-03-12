import pytest
from test.factories.user.factories import UserFactory
from test.factories.user.factories import TeamFactory
from test.factories.blog_post.factories import CategoryFactory
from django.test import Client
from rest_framework.test import APIClient



@pytest.fixture(autouse=True)
def create_team():
    return TeamFactory.create()

'''
@pytest.fixture(autouse=True)
def create_categories():
    return CategoryFactory.create()

@pytest.fixture(autouse=True)
def create_categories():
    return CategoryFactory.create()

@pytest.fixture(autouse=True)
def create_categories():
    return CategoryFactory.create()

@pytest.fixture(autouse=True)
def create_categories():
    return CategoryFactory.create()
'''

@pytest.fixture
def user_creation(autouse=True): 
    return UserFactory.create()


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def authenticated_client(client, user_creation):
    user = user_creation
    client.force_authenticate(user=user)
    return client
    
    
    