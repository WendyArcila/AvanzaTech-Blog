import pytest
import json
from rest_framework.test import APIClient
from post_cat_permission.models import PostCategoryPermission
from comment.models import BlogComments
from faker import Faker


fake = Faker()


@pytest.mark.django_db
def test_create_admin_user_can_create_a_comment_regardless_permissions(
        post_category_permissions1, client, user_admin, get_created_permission_none):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Team', 'Author', 'Authenticated']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    client.force_authenticate(user=user_admin)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 1


@pytest.mark.django_db
def test_create_authenticated_user_can_create_a_comment_when_authenticated_permission_read(
        post_category_permissions1, client, user_two, get_created_permission_none):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Team', 'Author']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    client.force_authenticate(user=user_two)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 1


@pytest.mark.django_db
def test_create_team_user_can_create_a_comment_when_team_permission_read(
        post_category_permissions1,
        get_created_permission_none,
        client,
        user_one,
        user_three):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Authenticated', 'Author']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }

    user_three.team = user_one.team
    client.force_authenticate(user=user_three)
    url = '/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 1


@pytest.mark.django_db
def test_create_author_user_can_create_a_comment_when_author_permission_read(
        post_category_permissions1, get_created_permission_none, client, user_one):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Authenticated', 'Team']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }

    client.force_authenticate(user=user_one)
    url = '/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 1


@pytest.mark.django_db
def test_create_authenticated_user_can_create_a_comment_when_authenticated_permission_edit(
        post_category_permissions1,
        client,
        user_two,
        get_created_permission_none,
        get_created_permission_edit):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Team', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Authenticated'
    ).update(permission=get_created_permission_edit)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    client.force_authenticate(user=user_two)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 1


@pytest.mark.django_db
def test_create_team_user_can_create_a_comment_when_team_permission_edit(
        post_category_permissions1,
        client,
        user_one,
        user_three,
        get_created_permission_none,
        get_created_permission_edit):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Authenticated', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Team'
    ).update(permission=get_created_permission_edit)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    user_three.team = user_one.team

    client.force_authenticate(user=user_three)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 1


@pytest.mark.django_db
def test_create_author_user_can_create_a_comment_when_author_permission_edit(
        post_category_permissions1,
        client,
        user_one,
        get_created_permission_none,
        get_created_permission_edit):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Authenticated', 'Team']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Author'
    ).update(permission=get_created_permission_edit)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    client.force_authenticate(user=user_one)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 1


@pytest.mark.django_db
def test_create_unauthenticated_user_cannot_create_a_comment_when_unauthenticated_permission_read(
        post_category_permissions1):

    client = APIClient()
    url = f'/comments/'
    json_data = {
        'blog_post': post_category_permissions1.id,
        'comment': fake.text()
    }
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "Authentication credentials were not provided." in response.data['detail']


@pytest.mark.django_db
def test_create_unauthenticated_user_cannot_create_a_comment_when_unauthenticated_permission_edit(
        post_category_permissions1, get_created_permission_edit):
    client = APIClient()
    url = f'/comments/'
    post_id = post_category_permissions1.id
    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Public'
    ).update(permission=get_created_permission_edit)
    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "Authentication credentials were not provided." in response.data['detail']


@pytest.mark.django_db
def test_create_authenticated_user_cannot_create_a_comment_without_information_in_comment(
        post_category_permissions1, client, user_admin):
    client.force_authenticate(user=user_admin)
    url = '/comments/'
    json_data = {
        'blog_post': post_category_permissions1.id,
        'comment': ""
    }
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 400, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "This field may not be blank." in response.data['comment']


@pytest.mark.django_db
def test_create_authenticated_user_cannot_create_a_comment_without_comment(
        post_category_permissions1, client, user_admin):
    client.force_authenticate(user=user_admin)
    url = '/comments/'
    json_data = {
        'blog_post': post_category_permissions1.id,
    }
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 400, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "This field is required." in response.data['comment']


@pytest.mark.django_db
def test_create_authenticated_user_cannot_create_a_comment_with_nonexistent_blog_post(
        client,
        user_admin):
    client.force_authenticate(user=user_admin)
    url = '/comments/'
    json_data = {
        'blog_post': 2,
        'comment': fake.text()
    }
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_authenticated_user_cannot_create_a_comment_without_blog_post(
        client, user_admin):
    client.force_authenticate(user=user_admin)
    url = '/comments/'
    json_data = {
        'comment': fake.text()
    }
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()
    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_authenticated_user_cannot_create_a_comment_when_authenticated_permission_is_None(
        post_category_permissions1, get_created_permission_none, client, user_two):

    post_id = post_category_permissions1.id
    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Authenticated'
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    client.force_authenticate(user=user_two)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_team_user_cannot_create_a_comment_when_team_permission_is_None(
        post_category_permissions1,
        get_created_permission_none,
        client,
        user_one,
        user_three):

    post_id = post_category_permissions1.id
    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Team'
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }
    user_three.team = user_one.team
    client.force_authenticate(user=user_three)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_author_user_cannot_create_a_comment_when_author_permission_is_None(
        post_category_permissions1, get_created_permission_none, client, user_one):

    post_id = post_category_permissions1.id
    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Author'
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
        'comment': fake.text()
    }

    client.force_authenticate(user=user_one)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert comments == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_update_put_authenticated_user_cannot_update_a_comment(
        post_category_permissions1,
        get_created_permission_none,
        client,
        user_one,
        user_two,
        comment_factory):

    post_id = post_category_permissions1.id
    comment = comment_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    json_data = {
        'blog_post': post_id,
        'comment': 'New Comment'
    }

    client.force_authenticate(user=user_two)
    url = f'/comments/{comment.id}/'
    response = client.put(url, json_data, format='json')

    assert response.status_code == 405, f"Error de solicitud: {response.content}"
    assert "Method \'PUT\' not allowed." in response.data['detail']


@pytest.mark.django_db
def test_update_patch_authenticated_user_cannot_update_a_comment(
        post_category_permissions1,
        get_created_permission_none,
        client,
        user_one,
        user_two,
        comment_factory):

    post_id = post_category_permissions1.id
    comment = comment_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    json_data = {
        'blog_post': post_id,
        'comment': 'New Comment'
    }

    client.force_authenticate(user=user_two)
    url = f'/comments/{comment.id}/'
    response = client.patch(url, json_data, format='json')

    assert response.status_code == 405, f"Error de solicitud: {response.content}"
    assert "Method \'PATCH\' not allowed." in response.data['detail']


@pytest.mark.django_db
def test_retrieve_authenticated_user_cannot_update_a_comment(
        post_category_permissions1,
        get_created_permission_none,
        client,
        user_one,
        user_two,
        comment_factory):

    comment = comment_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    client.force_authenticate(user=user_two)
    url = f'/comments/{comment.id}/'
    response = client.get(url)

    assert response.status_code == 405, f"Error de solicitud: {response.content}"
    assert "Method \'RETRIEVE\' not allowed." in response.data['detail']


@pytest.mark.django_db
def test_create_comment_different_users_can_comment_post(
        post_category_permissions1, client, user_one, user_admin, comment_factory):

    post_id = post_category_permissions1.id
    comment = comment_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)
    json_data = {
        'blog_post': post_id,
        'comment': 'New Comment'
    }

    client.force_authenticate(user=user_admin)
    url = f'/comments/'
    response = client.post(url, json_data, format='json')
    comments = BlogComments.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert comments == 2


@pytest.mark.django_db
def test_delete_authenticated_user_can_delete_a_comment_when_authenticated_user_is_the_author(
        post_category_permissions1, client, user_one, comment_factory):

    comment = comment_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    client.force_authenticate(user=user_one)
    url = f'/comments/{comment.id}/'
    response = client.delete(url, format='json')

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert "Object successfully deleted" in response.data['message']


@pytest.mark.django_db
def test_delete_team_user_cannot_delete_a_comment_when_authenticated_user_is_not_the_author(
        post_category_permissions1, user_three, client, user_one, comment_factory):

    comment = comment_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    client.force_authenticate(user=user_three)
    url = f'/comments/{comment.id}/'
    response = client.delete(url, format='json')

    assert response.status_code == 401, f"Error de solicitud: {response.content}"
    assert "Only author can delete this object" in response.data['message']


@pytest.mark.django_db
def test_pagination_works_with_60_likes(
        comment_factory,
        user_admin,
        post_category_permissions1):

    client = APIClient()
    client.force_authenticate(user=user_admin)
    comment_factory.create_batch(60, blog_post=post_category_permissions1)

    url = '/comments/'
    response = client.get(url)
    response_data = response.json()

    assert 'next' in response_data['links']
    assert 'previous' in response_data['links']
    assert response_data['count'] == 60
    assert response_data['total_pages'] == 6


@pytest.mark.django_db
def test_filtering_by_blog_post(
        comment_factory,
        user_admin,
        post_category_permissions1,
        post_category_permissions2):

    client = APIClient()
    client.force_authenticate(user=user_admin)
    comment_factory.create_batch(30, blog_post=post_category_permissions1)

    comment_factory.create_batch(30, blog_post=post_category_permissions2)

    url = '/comments/'
    response = client.get(url, {'blog_post': post_category_permissions1.id})
    response_data = response.json()

    assert response.status_code == 200
    assert response_data['count'] == 30


@pytest.mark.django_db
def test_filtering_by_user(
        comment_factory,
        user_admin,
        post_category_permissions1,
        post_category_permissions2):

    client = APIClient()
    client.force_authenticate(user=user_admin)
    like = comment_factory.create(
        author=user_admin,
        blog_post=post_category_permissions1)
    comment_factory.create_batch(30, blog_post=post_category_permissions1)

    comment_factory.create_batch(30, blog_post=post_category_permissions2)

    url = '/comments/'
    response = client.get(url, {'author': like.author.id})
    response_data = response.json()

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert response_data['count'] == 1
