import factory 

from user.models import CustomUser
from team.models import Team
from faker import Faker 
from factory import SubFactory

fake = Faker()

class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team 
        
    name = fake.name()
    description = fake.text()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta: 
        model = CustomUser
        
    email = 'usercommontest@test.com'
    nick_name = fake.name()
    password = 'test123456'
    team = SubFactory(TeamFactory)
    


