from factory.django import DjangoModelFactory
from user.models import CustomUser
from team.models import Team
import factory
from factory import SubFactory
from django.core.exceptions import ObjectDoesNotExist


class GetOrCreateFactory(DjangoModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        email = factory.Faker('email')
        try:
            model_class.objects.create(
                email=email, defaults=kwargs)[0]
        except ObjectDoesNotExist:
            return model_class.objects.create(
                email=email, **kwargs)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team
    name = factory.Faker('name')
    description = factory.Faker('text')


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker('email')
    nick_name = factory.Faker('name')
    password = 'test123456'
    team = SubFactory(TeamFactory)
    is_staff = False
    is_active = True
