from factory.django import DjangoModelFactory
from comment.models import BlogComments
import factory
from factory import SubFactory
from test.factories.user_team.factories import UserFactory


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = BlogComments

    comment = factory.Faker('text')
    author = SubFactory(UserFactory)
