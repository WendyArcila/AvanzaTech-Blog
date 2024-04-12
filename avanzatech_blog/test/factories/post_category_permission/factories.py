from factory.django import DjangoModelFactory
from post_cat_permission.models import PostCategoryPermission
from test.factories.category_permission.factories import CategoryFactory
from test.factories.category_permission.factories import PermissionFactory
from factory import SubFactory


class PostCategoryPermissionFactory(DjangoModelFactory):
    class Meta:
        model = PostCategoryPermission

    category = SubFactory(CategoryFactory)
    permission = SubFactory(PermissionFactory)
