import pytest
import json
from rest_framework.test import APIClient
from post_cat_permission.models import PostCategoryPermission
from post_like.models import PostLike
from faker import Faker

fake = Faker()


@pytest.mark.django_db
def test_create_like_admin_user_can_create_like_regardless_permissions(
        post_category_permissions1, client, user_admin, get_created_permission_none):
    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Team', 'Author', 'Authenticated']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }

    client.force_authenticate(user=user_admin)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 1


@pytest.mark.django_db
def test_create_like_authenticated_user_can_create_like_when_authenticated_permission_read(
        post_category_permissions1, client, user_two, get_created_permission_none):
    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Team', 'Author']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }

    client.force_authenticate(user=user_two)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 1


@pytest.mark.django_db
def test_create_like_team_user_can_create_like_when_team_permission_read(
        post_category_permissions1,
        client,
        user_three,
        user_one,
        get_created_permission_none):
    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Authenticated', 'Author']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }
    user_three.team = user_one.team
    client.force_authenticate(user=user_three)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 1


@pytest.mark.django_db
def test_create_like_author_user_can_create_like_when_author_permission_read(
        post_category_permissions1, client, user_one, get_created_permission_none):
    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name__in=['Authenticated', 'Team']
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }

    client.force_authenticate(user=user_one)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 1


@pytest.mark.django_db
def test_create_like_authenticated_user_can_create_like_when_authenticated_permission_edit(
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
    }

    client.force_authenticate(user=user_two)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 1


@pytest.mark.django_db
def test_create_like_team_user_can_create_like_when_team_permission_edit(
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
    }
    user_three.team = user_one.team
    client.force_authenticate(user=user_three)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 1


@pytest.mark.django_db
def test_create_like_author_user_can_create_like_when_author_permission_edit(
        post_category_permissions1,
        client,
        user_one,
        user_three,
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
    }

    client.force_authenticate(user=user_one)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 1


@pytest.mark.django_db
def test_create_like_unauthenticated_user_cannot_create_like_when_unauthenticated_permission_read(
        post_category_permissions1, get_created_permission_none, get_created_permission_edit):
    post_id = post_category_permissions1.id

    client = APIClient()
    json_data = {
        'blog_post': post_id,
    }
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "Authentication credentials were not provided." in response.data['detail']


@pytest.mark.django_db
def test_create_like_unauthenticated_user_cannot_create_like_when_unauthenticated_permission_read(
        post_category_permissions1, get_created_permission_none, get_created_permission_edit):
    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Public'
    ).update(permission=get_created_permission_edit)

    client = APIClient()
    json_data = {
        'blog_post': post_id,
    }
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "Authentication credentials were not provided." in response.data['detail']


@pytest.mark.django_db
def test_create_like_authenticated_user_cannot_create_like_without_blog_post(
        post_category_permissions1, get_created_permission_edit, user_admin, client):
    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Public'
    ).update(permission=get_created_permission_edit)

    client.force_authenticate(user=user_admin)
    json_data = {}
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_like_authenticated_user_cannot_create_like_with_nonexistent_blog_post(
        post_category_permissions1, get_created_permission_edit, client, user_admin):

    client.force_authenticate(user=user_admin)
    json_data = {
        'blog_post': 2,
    }
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_like_authenticated_user_cannot_create_a_like_when_authenticated_permission_is_None(
        post_category_permissions1, get_created_permission_none, client, user_two):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Authenticated'
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }
    client.force_authenticate(user=user_two)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_like_team_user_cannot_create_a_like_when_team_permission_is_None(
        post_category_permissions1, get_created_permission_none, client, user_one, user_three):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Team'
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }

    user_three.team = user_one.team
    client.force_authenticate(user=user_three)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_like_author_user_cannot_create_a_like_when_author_permission_is_None(
        post_category_permissions1, get_created_permission_none, client, user_one):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Author'
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }

    client.force_authenticate(user=user_one)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_like_author_user_cannot_create_a_like_when_author_permission_is_None(
        post_category_permissions1, get_created_permission_none, client, user_one):

    post_id = post_category_permissions1.id

    PostCategoryPermission.objects.filter(
        blog_post=post_id,
        category__name='Author'
    ).update(permission=get_created_permission_none)

    json_data = {
        'blog_post': post_id,
    }

    client.force_authenticate(user=user_one)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 404, f"Error de solicitud: {response.content}"
    assert likes == 0
    assert "No BlogPost matches the given query." in response.data['detail']


@pytest.mark.django_db
def test_create_like_same_user_cannot_like_post_twice(
        post_category_permissions1, like_factory, client, user_one):

    post_id = post_category_permissions1.id
    like = like_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    json_data = {
        'blog_post': post_id,
    }

    client.force_authenticate(user=user_one)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 400, f"Error de solicitud: {response.content}"
    assert likes == 1
    assert "This post already has your like." in response.data['non_field_errors']


@pytest.mark.django_db
def test_create_like_different_users_can_like_post(
        post_category_permissions1,
        like_factory,
        client,
        user_one,
        user_three):

    post_id = post_category_permissions1.id
    like = like_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    json_data = {
        'blog_post': post_id,
    }

    client.force_authenticate(user=user_three)
    url = f'/likes/'
    response = client.post(url, json_data, format='json')
    likes = PostLike.objects.count()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert likes == 2


@pytest.mark.django_db
def test_update_put_authenticated_user_cannot_update_like(
        post_category_permissions1, client, user_one, user_two, like_factory):

    like = like_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    json_data = {
        'blog_post': post_category_permissions1.id,
    }

    client.force_authenticate(user=user_two)
    url = f'/likes/{like.id}/'
    response = client.put(url, json_data, format='json')

    assert response.status_code == 405, f"Error de solicitud: {response.content}"
    assert "Method \'PUT\' not allowed." in response.data['detail']


@pytest.mark.django_db
def test_update_patch_authenticated_user_cannot_update_like(
        post_category_permissions1, client, user_one, user_two, like_factory):

    like = like_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    json_data = {
        'blog_post': post_category_permissions1.id,
    }

    client.force_authenticate(user=user_two)
    url = f'/likes/{like.id}/'
    response = client.patch(url, json_data, format='json')

    assert response.status_code == 405, f"Error de solicitud: {response.content}"
    assert "Method \'PATCH\' not allowed." in response.data['detail']


@pytest.mark.django_db
def test_get_retrieve_authenticated_user_cannot_update_like(
        post_category_permissions1, client, user_one, user_two, like_factory):

    like = like_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    json_data = {
        'blog_post': post_category_permissions1.id,
    }

    client.force_authenticate(user=user_two)
    url = f'/likes/{like.id}/'
    response = client.get(url)

    assert response.status_code == 405, f"Error de solicitud: {response.content}"
    assert "Method \'RETRIEVE\' not allowed." in response.data['detail']


@pytest.mark.django_db
def test_delete_authenticated_user_can_delete_like_when_authenticated_user_is_the_author(
        post_category_permissions1, client, user_one, user_two, like_factory):

    like = like_factory.create(
        author=user_two,
        blog_post=post_category_permissions1)

    client.force_authenticate(user=user_two)
    url = f'/likes/{like.id}/'
    response = client.delete(url)

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert "Object successfully deleted" in response.data['message']


@pytest.mark.django_db
def test_delete_authenticated_user_cannot_delete_like_when_authenticated_user_is_not_the_author(
        post_category_permissions1, client, user_one, user_two, like_factory):

    like = like_factory.create(
        author=user_one,
        blog_post=post_category_permissions1)

    client.force_authenticate(user=user_two)
    url = f'/likes/{like.id}/'
    response = client.delete(url)

    assert response.status_code == 401, f"Error de solicitud: {response.content}"
    assert "Only author can delete this object" in response.data['message']


@pytest.mark.django_db
def test_pagination_works_with_60_likes(
        like_factory,
        user_admin,
        post_category_permissions1):

    client = APIClient()
    client.force_authenticate(user=user_admin)
    like_factory.create_batch(60, blog_post=post_category_permissions1)

    url = '/likes/'
    response = client.get(url)
    response_data = response.json()

    assert 'next' in response_data['links']
    assert 'previous' in response_data['links']
    assert response_data['count'] == 60
    assert response_data['total_pages'] == 3


@pytest.mark.django_db
def test_filtering_by_blog_post(
        like_factory,
        user_admin,
        post_category_permissions1,
        post_category_permissions2):

    client = APIClient()
    client.force_authenticate(user=user_admin)
    like_factory.create_batch(30, blog_post=post_category_permissions1)

    like_factory.create_batch(30, blog_post=post_category_permissions2)

    url = '/likes/'
    response = client.get(url, {'blog_post': post_category_permissions1.id})
    response_data = response.json()

    assert response.status_code == 200
    assert response_data['count'] == 30


@pytest.mark.django_db
def test_filtering_by_user(
        like_factory,
        user_admin,
        post_category_permissions1,
        post_category_permissions2):

    client = APIClient()
    client.force_authenticate(user=user_admin)
    like = like_factory.create(
        author=user_admin,
        blog_post=post_category_permissions1)
    like_factory.create_batch(30, blog_post=post_category_permissions1)

    like_factory.create_batch(30, blog_post=post_category_permissions2)

    url = '/likes/'
    response = client.get(url, {'author': like.author.id})
    response_data = response.json()

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert response_data['count'] == 1
