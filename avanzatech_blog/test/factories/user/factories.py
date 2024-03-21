from factory.django import DjangoModelFactory
from user.models import CustomUser
from team.models import Team
from faker import Faker 
from factory import SubFactory


fake = Faker()

class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team 
        
    name = fake.name()
    description = fake.text()

class UserFactory(DjangoModelFactory):
    class Meta: 
        model = CustomUser
        
    email = 'testuser@test.com'
    nick_name = fake.name()
    password = 'test123456'
    team = SubFactory(TeamFactory)
    
    

class UserTwoFactory(DjangoModelFactory):
    class Meta: 
        model = CustomUser
        
    email = 'testuser2@test.com'
    nick_name = fake.name()
    password = 'test123456'
    team = SubFactory(TeamFactory)
    

class UserThreeFactory(DjangoModelFactory):
    class Meta: 
        model = CustomUser
        
    email = 'testuser3@test.com'
    nick_name = fake.name()
    password = 'test123456'
    team = SubFactory(TeamFactory)