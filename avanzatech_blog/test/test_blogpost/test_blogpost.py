import pytest
import json
from faker import Faker
from rest_framework.test import APIClient
from post_cat_permission.models import PostCategoryPermission
from blog_post.models import BlogPost
from django.urls import reverse


fake = Faker()


@pytest.mark.django_db
def test_post_creation_post_successfully(
        client,
        user_one,
        get_created_category_public,
        get_created_category_authenticated,
        get_created_category_team,
        get_created_category_author,
        get_created_permission_read):

    json_data = {
        "title": fake.name(),
        "content": fake.text(max_nb_chars=500),
        "post_category_permission": [
            {"permission": get_created_permission_read.id, "category": get_created_category_public.id},
            {"permission": get_created_permission_read.id, "category": get_created_category_authenticated.id},
            {"permission": get_created_permission_read.id, "category": get_created_category_team.id},
            {"permission": get_created_permission_read.id, "category": get_created_category_author.id},
        ],
    }

    url = '/blogpost/'
    client.force_authenticate(user=user_one)
    response = client.post(
        url, json.dumps(json_data), content_type='application/json')

    blogpost = BlogPost.objects.all().first()

    assert response.status_code == 201, f"Error de solicitud: {response.content}"
    assert PostCategoryPermission.objects.count() == 4
    assert blogpost.content[:200] == blogpost.excerpt
    for post_category_permission in PostCategoryPermission.objects.filter(
            blog_post=blogpost):
        assert post_category_permission.blog_post == blogpost


@pytest.mark.django_db
def test_post_an_unauthenticated_user_can_not_create_a_post_and_a_403_is_returned(
        client,
        get_created_category_public,
        get_created_category_authenticated,
        get_created_category_team,
        get_created_category_author,
        get_created_permission_read):

    current_posts = BlogPost.objects.count()
    json_data = {
        "title": fake.name(),
        "content": fake.text(max_nb_chars=500),
        "post_category_permission": [
            {"permission": get_created_permission_read.id, "category": get_created_category_public.id},
            {"permission": get_created_permission_read.id, "category": get_created_category_authenticated.id},
            {"permission": get_created_permission_read.id, "category": get_created_category_team.id},
            {"permission": get_created_permission_read.id, "category": get_created_category_author.id},
        ],
    }

    url = '/blogpost/'
    response = client.post(
        url, json.dumps(json_data), content_type='application/json')
    auth_response = response.data.get('detail').code

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert auth_response == "not_authenticated"
    assert BlogPost.objects.count() == current_posts


@pytest.mark.django_db
def test_post_creation_post_with_insufficient_data(
        client,
        user_one,
        get_created_category_public,
        get_created_category_authenticated,
        get_created_category_team,
        get_created_category_author,
        get_created_permission_read):

    client.force_authenticate(user=user_one)
    data = [
        {
            "content": fake.text(max_nb_chars=500),
            "post_category_permission": [
                {"permission": get_created_permission_read.id, "category": get_created_category_public.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_authenticated.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_team.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_author.id},
            ],
        },
        {
            "title": fake.name(),
            "post_category_permission": [
                {"permission": get_created_permission_read.id, "category": get_created_category_public.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_authenticated.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_team.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_author.id},
            ],
        },
        {
            "title": fake.name(),
            "content": fake.text(max_nb_chars=500)
        },
        {
            "title": fake.name(),
            "content": fake.text(max_nb_chars=500),
            "post_category_permission": []
        },
        {
            "title": fake.name(),
            "content": fake.text(max_nb_chars=500),
            "post_category_permission": [
                {"permission": get_created_permission_read.id, "category": get_created_category_public.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_authenticated.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_team.id}
            ],
        },
        {
            "title": fake.name(),
            "content": fake.text(max_nb_chars=500),
            "post_category_permission": [
                {"permission": get_created_permission_read.id, "category": get_created_category_public.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_authenticated.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_team.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_author.id},
                {"permission": get_created_permission_read.id, "category": get_created_category_author.id},
            ],
        }
    ]

    url = '/blogpost/'
    for i, json_data in enumerate(data, start=1):
        response = client.post(
            url,
            json.dumps(json_data),
            content_type='application/json')
        assert response.status_code == 400
        if i == 1:
            assert "This field is required." in response.data['title']
        elif i == 2:
            assert "This field is required." in response.data['content']
        elif i == 3:
            assert "This field is required." in response.data['post_category_permission']
        elif i == 4:
            assert "Permission are necessary to create a post." in response.data[
                'non_field_errors']
        elif i == 5 or i == 6:
            assert "The post needs exactly four permissions." in response.data['non_field_errors']


@pytest.mark.django_db
def test_get_admin_user_can_see_all_posts_regardless_posts_permissions(
        client, user_admin, post_category_permissions, get_created_permission_none):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions)]],
        category__name__in=['Authenticated', 'Team', 'Author', 'Public']
    ).update(permission=get_created_permission_none)

    url = '/blogpost/'
    client.force_authenticate(user=user_admin)
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 8


@pytest.mark.django_db
def test_get_unauthenticated_user_can_see_only_public_posts_when_posts_have_public_read_permission(
        client, post_category_permissions, get_created_permission_none):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Authenticated', 'Team', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Public'
    ).update(permission=get_created_permission_none)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_get_unauthenticated_user_can_see_only_public_posts_when_posts_have_public_edit_permission(
        client, post_category_permissions, get_created_permission_none, get_created_permission_edit):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Authenticated', 'Team', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name='Public'
    ).update(permission=get_created_permission_edit)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Public'
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name__in=['Authenticated', 'Team', 'Author']
    ).update(permission=get_created_permission_edit)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_get_authenticated_user_can_see_only_authenticated_posts_when_posts_have_authenticated_read_permission(
        client, user_one, user_two, post_category_permissions, get_created_permission_none):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Public', 'Team', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Authenticated'
    ).update(permission=get_created_permission_none)

    url = '/blogpost/'
    client.force_authenticate(user=user_two)
    response = client.get(url)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert user_two.team != user_one.team
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_get_authenticated_user_can_see_only_authenticated_posts_when_posts_have_authenticated_edit_permission(
        client, user_one, user_two, post_category_permissions, get_created_permission_none, get_created_permission_edit):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Public', 'Team', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name='Authenticated'
    ).update(permission=get_created_permission_edit)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Authenticated'
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name__in=['Public', 'Team', 'Author']
    ).update(permission=get_created_permission_edit)

    url = '/blogpost/'
    client.force_authenticate(user=user_two)
    response = client.get(url)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert user_two.team != user_one.team
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_get_authenticated_user_with_the_same_team_can_read_post_when_posts_have_team_read_permission(
        client, user_one, user_three, post_category_permissions, get_created_permission_none):
    user_three.team = user_one.team

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Public', 'Authenticated', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Team'
    ).update(permission=get_created_permission_none)

    client.force_authenticate(user=user_three)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_get_authenticated_user_with_the_same_team_can_read_post_when_posts_have_team_edit_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):
    user_three.team = user_one.team

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Public', 'Authenticated', 'Author']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name='Team'
    ).update(permission=get_created_permission_edit)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Team'
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name__in=['Public', 'Authenticated', 'Author']
    ).update(permission=get_created_permission_edit)

    client.force_authenticate(user=user_three)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_get_author_user_can_read_post_when_posts_have_author_read_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_none):
    user_three.team = user_one.team

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Public', 'Authenticated', 'Team']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Author'
    ).update(permission=get_created_permission_none)

    client.force_authenticate(user=user_one)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_get_author_user_can_read_post_when_posts_have_author_edit_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):

    user_three.team = user_one.team

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name__in=['Public', 'Authenticated', 'Team']
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[:len(post_category_permissions) // 2]],
        category__name='Author'
    ).update(permission=get_created_permission_edit)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name='Author'
    ).update(permission=get_created_permission_none)

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[len(post_category_permissions) // 2:]],
        category__name__in=['Public', 'Authenticated', 'Team']
    ).update(permission=get_created_permission_edit)

    client.force_authenticate(user=user_one)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 4


@pytest.mark.django_db
def test_retrieve_admin_user_can_read_post_regardless_post_permissions(
        client, user_admin, post_category_permissions, get_created_permission_none):

    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Author', 'Public', 'Team', 'Public'])

    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_admin)
    response = client.get(url)
    response_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == response_data['id']


@pytest.mark.django_db
def test_retrieve_authenticated_user_can_read_post_when_the_post_have_authenticated_read_permission(
        client, user_two, post_category_permissions, get_created_permission_none):

    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended,
        category__name__in=['Author', 'Public', 'Team']
    )

    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_two)
    response = client.get(url)
    response_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == response_data['id']


@pytest.mark.django_db
def test_retrieve_authenticated_user_can_read_post_when_the_post_have_authenticated_edit_permission(
        client, user_two, post_category_permissions, get_created_permission_none, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended,
        category__name__in=['Author', 'Public', 'Team']
    )

    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update_authenticated = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in='Authenticated')

    post_category_permissions_to_update_authenticated.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_two)
    response = client.get(url)
    response_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == response_data['id']


@pytest.mark.django_db
def test_retrieve_team_user_can_read_post_when_the_post_have_team_read_permission(
        client, user_one, user_three, post_category_permissions, get_created_permission_none):

    user_three.team = user_one.team
    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Author', 'Authenticated', 'Public'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_three)
    response = client.get(url)
    responde_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == responde_data['id']


@pytest.mark.django_db
def test_retrieve_team_user_can_read_post_when_the_post_have_team_edit_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):

    user_three.team = user_one.team
    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Author', 'Authenticated', 'Public'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update_team = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in='Team')
    post_category_permissions_to_update_team.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_three)
    response = client.get(url)
    responde_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == responde_data['id']


@pytest.mark.django_db
def test_retrieve_author_user_can_read_post_when_the_post_have_author_read_permission(
        client, user_one, post_category_permissions, get_created_permission_none):

    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Public'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.get(url)
    responde_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == responde_data['id']


@pytest.mark.django_db
def test_retrieve_author_user_can_read_post_when_the_post_have_author_edit_permission(
        client,
        user_one,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Public'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Author')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.get(url)
    responde_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == responde_data['id']


@pytest.mark.django_db
def test_retrieve_public_user_can_read_post_when_the_post_have_public_edit_permission(
        post_category_permissions, get_created_permission_none, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Public')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client = APIClient()
    response = client.get(url)
    responde_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == responde_data['id']


@pytest.mark.django_db
def test_retrieve_public_user_can_read_post_when_the_post_have_author_read_permission(
        post_category_permissions, get_created_permission_none):

    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    url = f'/blogpost/{blog_post_sended.id}/'
    client = APIClient()
    response = client.get(url)
    responde_data = response.json()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blog_post_sended.id == responde_data['id']


@pytest.mark.django_db
def test_get_public_user_cannot_read_post_when_posts_have_not_public_read_and_edit_permission(
        post_category_permissions, get_created_permission_none,):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[0:len(post_category_permissions)]],
        category__name='Public'
    ).update(permission=get_created_permission_none)

    client = APIClient()

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_get_authenticated_user_cannot_read_and_edit_post_when_posts_have_not_authenticated_read_and_edit_permission(
        post_category_permissions, user_two, client, get_created_permission_none,):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[0:len(post_category_permissions)]],
        category__name='Authenticated'
    ).update(permission=get_created_permission_none)

    client.force_authenticate(user=user_two)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_get_team_user_cannot_read_and_edit_post_when_posts_have_not_team_read_and_edit_permission(
        post_category_permissions, user_one, user_three, client, get_created_permission_none,):

    user_three.team = user_one.team
    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[0:len(post_category_permissions)]],
        category__name='Team'
    ).update(permission=get_created_permission_none)

    client.force_authenticate(user=user_three)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_get_author_user_cannot_read_and_edit_post_when_posts_have_not_author_read_and_edit_permission(
        post_category_permissions, user_one, client, get_created_permission_none,):

    PostCategoryPermission.objects.filter(
        blog_post__in=[post.id for post in post_category_permissions[0:len(post_category_permissions)]],
        category__name='Author'
    ).update(permission=get_created_permission_none)

    client.force_authenticate(user=user_one)

    url = '/blogpost/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_update_blogpost_admin_user_can_edit_post_regardless_post_permissions(
        user_admin, client, post_category_permissions, get_created_permission_none):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Author', 'Public'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_admin)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blogpost.title != responde_data['title']


@pytest.mark.django_db
def test_update_blogpost_unauthenticated_user_can_edit_post_when_posts_have_unauthenticated_edit_permission(
        post_category_permissions, get_created_permission_none, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Public')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }

    url = f'/blogpost/{blog_post_sended.id}/'
    client = APIClient()
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blogpost.title != responde_data['title']


@pytest.mark.django_db
def test_update_blogpost_authenticated_user_can_edit_post_when_posts_have_authenticated_edit_permission(
        client, user_two, post_category_permissions, get_created_permission_none, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Public', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Authenticated')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_two)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blogpost.title != responde_data['title']


@pytest.mark.django_db
def test_update_blogpost_team_user_can_edit_post_when_posts_have_team_edit_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Team')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }
    user_three.team = user_one.team

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_three)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blogpost.title != responde_data['title']


@pytest.mark.django_db
def test_update_blogpost_author_user_can_edit_post_when_posts_have_author_edit_permission(
        client,
        user_one,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Team'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Author')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert blogpost.title != responde_data['title']


@pytest.mark.django_db
def test_update_permissions_through_blogpost(
        client,
        user_admin,
        post_category_permissions,
        get_created_permission_none):

    blog_post_sended = post_category_permissions[0]
    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]
    permission = post_category_permissions_data[0]
    permission['permission'] = get_created_permission_none.id
    json_data = {
        "author": blog_post_sended.author.id,
        "title": blog_post_sended.title,
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }
    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_admin)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    response_data = response.json()

    updated_permissions = response_data.get('post_category_permission', [])

    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert updated_permissions == post_category_permissions_data


@pytest.mark.django_db
def test_update_blogpost_unauthenticated_user_cannot_edit_post_when_posts_have_unauthenticated_read_permission(
        post_category_permissions, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Author', 'Team'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }

    url = f'/blogpost/{blog_post_sended.id}/'
    client = APIClient()
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert blogpost.title == BlogPost.objects.filter(
        id=blogpost.id).first().title
    assert "You do not have permission to edit this post." in response.data['detail']


@pytest.mark.django_db
def test_update_blogpost_authenticated_user_cannot_edit_post_when_posts_have_authenticated_read_permission(
        client, user_two, post_category_permissions, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Public', 'Author', 'Team'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_two)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert blogpost.title == BlogPost.objects.filter(
        id=blogpost.id).first().title
    assert "You do not have permission to edit this post." in response.data['detail']


@pytest.mark.django_db
def test_update_blogpost_team_user_cannot_edit_post_when_posts_have_team_read_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Public', 'Author', 'Authenticated'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }
    user_three.team = user_one.team
    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_three)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')
    responde_data = response.json()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert blogpost.title == BlogPost.objects.filter(
        id=blogpost.id).first().title
    assert "You do not have permission to edit this post." in response.data['detail']


@pytest.mark.django_db
def test_update_blogpost_author_user_cannot_edit_post_when_posts_have_author_read_permission(
        client, user_one, post_category_permissions, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    blogpost = BlogPost.objects.all().first()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Public', 'Team', 'Authenticated'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    json_data = {
        "author": blog_post_sended.author.id,
        "title": 'New Title',
        "content": blog_post_sended.content,
        "post_category_permission": post_category_permissions_data
    }

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.patch(
        url, json.dumps(json_data), content_type='application/json')

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert blogpost.title == BlogPost.objects.filter(
        id=blogpost.id).first().title
    assert "You do not have permission to edit this post." in response.data['detail']


@pytest.mark.django_db
def test_update_post_with_insufficient_data(
        client,
        user_admin,
        post_category_permissions):

    blog_post_sended = post_category_permissions[0]

    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    post_category_permissions_data = [
        {"category": perm.category_id, "permission": perm.permission_id}
        for perm in permissions
    ]

    client.force_authenticate(user=user_admin)
    data = [
        {
            "author": blog_post_sended.author.id,
            "title": 'New Title',
            "content": blog_post_sended.content,
        },
        {
            "author": blog_post_sended.author.id,
            "title": 'New Title',
            "content": blog_post_sended.content,
            "post_category_permission": []
        },
        {
            "author": blog_post_sended.author.id,
            "title": 'New Title',
            "content": blog_post_sended.content,
            "post_category_permission": post_category_permissions_data[0]
        }
    ]

    url = f'/blogpost/{blog_post_sended.id}/'
    for i, json_data in enumerate(data, start=1):
        response = client.put(
            url,
            json.dumps(json_data),
            content_type='application/json')
        assert response.status_code == 400, f"Error de solicitud: {response.content}"
        if i == 1:
            assert "Permission are necessary to create a post." in response.data[
                'non_field_errors']
        elif i == 2:
            assert "Permission are necessary to create a post." in response.data[
                'non_field_errors']
        elif i == 3:
            assert "non_field_errors" in response.data['post_category_permission']


@pytest.mark.django_db
def test_delete_blogpost_admin_user_can_delete_post_regardless_post_permissions(
        user_admin, client, post_category_permissions, get_created_permission_none):

    total_post_before = BlogPost.objects.count()
    blog_post_sended = post_category_permissions[0]

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Author', 'Public'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_admin)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert total_post_after != total_post_before


@pytest.mark.django_db
def test_delete_blogpost_unauthenticated_user_can_delete_post_when_posts_have_unauthenticated_edit_permission(
        post_category_permissions, get_created_permission_none, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    total_post_before = BlogPost.objects.count()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Public')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client = APIClient()
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert total_post_after != total_post_before


@pytest.mark.django_db
def test_delete_blogpost_authenticated_user_can_edit_post_when_posts_have_authenticated_edit_permission(
        client, user_two, post_category_permissions, get_created_permission_none, get_created_permission_edit):

    total_post_before = BlogPost.objects.count()
    blog_post_sended = post_category_permissions[0]
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Public', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Authenticated')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_two)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert total_post_after != total_post_before


@pytest.mark.django_db
def test_delete_blogpost_team_user_can_edit_post_when_posts_have_team_edit_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):

    total_post_before = BlogPost.objects.count()
    blog_post_sended = post_category_permissions[0]
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Team')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    user_three.team = user_one.team
    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_three)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert total_post_after != total_post_before


@pytest.mark.django_db
def test_delete_blogpost_author_user_can_edit_post_when_posts_have_author_edit_permission(
        client,
        user_one,
        post_category_permissions,
        get_created_permission_none,
        get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    total_post_before = BlogPost.objects.count()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Team'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_none)

    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name='Author')
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert total_post_after != total_post_before


@pytest.mark.django_db
def test_delete_permissions_through_blogpost(
        client,
        user_admin,
        post_category_permissions):

    total_permissions_before = PostCategoryPermission.objects.count()
    blog_post_sended = post_category_permissions[0]
    permissions = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_admin)
    response = client.delete(url)

    total_permissions_after = PostCategoryPermission.objects.count()

    assert response.status_code == 204, f"Error de solicitud: {response.content}"
    assert total_permissions_after != total_permissions_before


@pytest.mark.django_db
def test_delete_blogpost_unauthenticated_user_cannot_edit_post_when_posts_have_unauthenticated_read_permission(
        post_category_permissions, get_created_permission_edit, get_created_permission_read):

    blog_post_sended = post_category_permissions[0]
    total_post_before = BlogPost.objects.count()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Authenticated', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client = APIClient()
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert "You do not have permission to delete this post." in response.data['detail']
    assert total_post_after == total_post_before


@pytest.mark.django_db
def test_delete_blogpost_authenticated_user_cannot_edit_post_when_posts_have_authenticated_read_permission(
        client, user_two, post_category_permissions, get_created_permission_edit):

    total_post_before = BlogPost.objects.count()
    blog_post_sended = post_category_permissions[0]
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Team', 'Public', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_two)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert "You do not have permission to delete this post." in response.data['detail']
    assert total_post_after == total_post_before


@pytest.mark.django_db
def test_delete_blogpost_team_user_cannot_edit_post_when_posts_have_team_read_permission(
        client,
        user_one,
        user_three,
        post_category_permissions,
        get_created_permission_edit):

    total_post_before = BlogPost.objects.count()
    blog_post_sended = post_category_permissions[0]
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Author'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    user_three.team = user_one.team
    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_three)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert "You do not have permission to delete this post." in response.data['detail']
    assert total_post_after == total_post_before


@pytest.mark.django_db
def test_delete_blogpost_author_user_cannot_edit_post_when_posts_have_author_read_permission(
        client, user_one, post_category_permissions, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    total_post_before = BlogPost.objects.count()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Team'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert "You do not have permission to delete this post." in response.data['detail']
    assert total_post_after == total_post_before


@pytest.mark.django_db
def test_delete_blogpost_author_user_cannot_edit_post_when_posts_have_author_read_permission(
        client, user_one, post_category_permissions, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    total_post_before = BlogPost.objects.count()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Team'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert "You do not have permission to delete this post." in response.data['detail']
    assert total_post_after == total_post_before


@pytest.mark.django_db
def test_delete_blogpost_author_user_cannot_edit_post_when_posts_have_author_read_permission(
        client, user_one, post_category_permissions, get_created_permission_edit):

    blog_post_sended = post_category_permissions[0]
    total_post_before = BlogPost.objects.count()
    post_category_permissions_to_update = PostCategoryPermission.objects.filter(
        blog_post=blog_post_sended, category__name__in=[
            'Authenticated', 'Public', 'Team'])
    post_category_permissions_to_update.update(
        permission=get_created_permission_edit)

    url = f'/blogpost/{blog_post_sended.id}/'
    client.force_authenticate(user=user_one)
    response = client.delete(url)
    total_post_after = BlogPost.objects.count()

    assert response.status_code == 403, f"Error de solicitud: {response.content}"
    assert "You do not have permission to delete this post." in response.data['detail']
    assert total_post_after == total_post_before


@pytest.mark.django_db
def test_pagination_works_with_30_post(post_category_permissions30):
    client = APIClient()
    url = '/blogpost/'
    response = client.get(url)
    response_data = response.json()

    assert 'next' in response_data['links']
    assert 'previous' in response_data['links']
    assert response_data['count'] == 30
    assert response_data['total_pages'] == 3
