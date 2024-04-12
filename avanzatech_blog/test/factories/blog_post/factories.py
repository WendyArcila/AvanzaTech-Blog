
import factory
from factory.django import DjangoModelFactory
from blog_post.models import BlogPost
from test.factories.post_category_permission.factories import PostCategoryPermissionFactory
from test.factories.category_permission.factories import CategoryFactory, PermissionFactory
from test.factories.user_team.factories import UserFactory
from factory import SubFactory


class BlogPostFactory(DjangoModelFactory):
    class Meta:
        model = BlogPost
        skip_postgeneration_save = True

    title = factory.Faker('name')
    content = factory.Faker('text', max_nb_chars=500)

    @factory.post_generation
    def set_author(self, create, extracted, **kwargs):
        if extracted:
            self.author = extracted
            self.save()
