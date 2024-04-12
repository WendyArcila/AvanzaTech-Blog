
from factory.django import DjangoModelFactory
from post_like.models import PostLike
from test.factories.user_team.factories import UserFactory
from factory import SubFactory


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = PostLike

    author = SubFactory(UserFactory)
