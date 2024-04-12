import pytest
from test.factories.user_team.factories import UserFactory, TeamFactory
from test.factories.category_permission.factories import CategoryFactory, PermissionFactory
from test.factories.blog_post.factories import BlogPostFactory
from test.factories.post_category_permission.factories import PostCategoryPermissionFactory
from test.factories.comments.factories import CommentFactory
from test.factories.likes.factories import LikeFactory
from rest_framework.test import APIClient
from pytest_factoryboy import register

register(UserFactory)
register(TeamFactory)
register(CategoryFactory)
register(PermissionFactory)
register(BlogPostFactory)
register(PostCategoryPermissionFactory)
register(CommentFactory)
register(LikeFactory)


@pytest.fixture()
def get_created_team(db):
    team = TeamFactory.create(id=1)
    return team


@pytest.fixture()
def get_created_category_public(db):
    category = CategoryFactory.create(name='Public')
    return category


@pytest.fixture()
def get_created_category_authenticated(db):
    category = CategoryFactory.create(name='Authenticated')
    return category


@pytest.fixture()
def get_created_category_team(db):
    category = CategoryFactory.create(name='Team')
    return category


@pytest.fixture()
def get_created_category_author(db):
    category = CategoryFactory.create(name='Author')
    return category


@pytest.fixture()
def get_created_permission_read(db):
    permission = PermissionFactory.create(name='ReadOnly')
    return permission


@pytest.fixture()
def get_created_permission_edit(db):
    permission = PermissionFactory.create(name='Edit')
    return permission


@pytest.fixture()
def get_created_permission_none(db):
    permission = PermissionFactory.create(name='None')
    return permission


@pytest.fixture
def user_one(db, user_factory):
    return user_factory.create()


@pytest.fixture
def user_two(db, user_factory):
    return user_factory.create(email='user2@test.com')


@pytest.fixture
def user_three(db, user_factory):
    return user_factory.create(email='user3@test.com')


@pytest.fixture
def user_admin(db, user_factory):
    return user_factory.create(
        email='admin@test.com',
        is_staff=True,
        is_superuser=True)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def post_category_permissions(
        db,
        request,
        client,
        user_one,
        post_category_permission_factory,
        get_created_category_public,
        get_created_category_authenticated,
        get_created_category_team,
        get_created_category_author,
        get_created_permission_read,
        blog_post_factory):

    client.force_authenticate(user=user_one)

    new_blogposts = [
        blog_post_factory.create(
            author=user_one) for _ in range(8)]

    for post in new_blogposts:
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_public,
            permission=get_created_permission_read)
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_authenticated,
            permission=get_created_permission_read)
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_team,
            permission=get_created_permission_read)
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_author,
            permission=get_created_permission_read)

    return new_blogposts


@pytest.fixture
def post_category_permissions30(
        db,
        request,
        client,
        user_one,
        post_category_permission_factory,
        get_created_category_public,
        get_created_category_authenticated,
        get_created_category_team,
        get_created_category_author,
        get_created_permission_read,
        blog_post_factory):

    client.force_authenticate(user=user_one)

    new_blogposts = [
        blog_post_factory.create(
            author=user_one) for _ in range(30)]

    for post in new_blogposts:
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_public,
            permission=get_created_permission_read)
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_authenticated,
            permission=get_created_permission_read)
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_team,
            permission=get_created_permission_read)
        post_category_permission_factory(
            blog_post=post,
            category=get_created_category_author,
            permission=get_created_permission_read)

    return new_blogposts


@pytest.fixture
def post_category_permissions1(
        db,
        request,
        client,
        user_one,
        post_category_permission_factory,
        get_created_category_public,
        get_created_category_authenticated,
        get_created_category_team,
        get_created_category_author,
        get_created_permission_edit,
        blog_post_factory):

    client.force_authenticate(user=user_one)

    new_blogposts = blog_post_factory.create(
        author=user_one)

    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_public,
        permission=get_created_permission_edit)
    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_authenticated,
        permission=get_created_permission_edit)
    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_team,
        permission=get_created_permission_edit)
    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_author,
        permission=get_created_permission_edit)

    return new_blogposts


@pytest.fixture
def post_category_permissions2(
        db,
        request,
        client,
        user_one,
        post_category_permission_factory,
        get_created_category_public,
        get_created_category_authenticated,
        get_created_category_team,
        get_created_category_author,
        get_created_permission_edit,
        blog_post_factory):

    client.force_authenticate(user=user_one)

    new_blogposts = blog_post_factory.create(
        author=user_one)

    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_public,
        permission=get_created_permission_edit)
    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_authenticated,
        permission=get_created_permission_edit)
    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_team,
        permission=get_created_permission_edit)
    post_category_permission_factory(
        blog_post=new_blogposts,
        category=get_created_category_author,
        permission=get_created_permission_edit)

    return new_blogposts
