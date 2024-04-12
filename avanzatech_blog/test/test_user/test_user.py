import pytest
import json
from rest_framework.reverse import reverse
from user.models import CustomUser
from team.models import Team
from rest_framework.test import APIClient
from django.contrib.sessions.backends.db import SessionStore
from test.factories.user_team.factories import TeamFactory


@pytest.mark.django_db
def test_user_team_deleted_default_one(
        get_created_team,
        user_factory,
        team_factory):
    team = get_created_team
    team2 = team_factory.create()
    user = user_factory(team=team2)
    team = Team.objects.filter(id=team2.id).first()
    team.delete()
    user.refresh_from_db()
    assert user.team.id == 1


@pytest.mark.django_db
def test_new_common_user(user_factory):
    user = user_factory.create()
    assert CustomUser.objects.all().count() == 1
    assert user.is_staff == False
    assert user.is_active


@pytest.mark.django_db
def test_new_admin_user(user_admin, get_created_team):
    user = CustomUser.objects.all().first()
    user_admin_created_by_db = CustomUser.objects.create_superuser(
        email='email@test.co', team=get_created_team, is_staff=True, is_superuser=True)

    assert user_admin_created_by_db.is_superuser == user_admin.is_superuser
    assert user_admin_created_by_db.is_staff == user_admin.is_staff
    assert user_admin.is_superuser == user.is_superuser
    assert user_admin.is_staff == user.is_staff


@pytest.mark.django_db
def test_login_user_successfully():
    team = TeamFactory.create()
    user = CustomUser.objects.create_user(
        email='login@test.co',
        password='user123456',
        nick_name='nick',
        team=team)
    json_data = {
        "username": user.email,
        "password": 'user123456'
    }

    url = reverse('login')
    client = APIClient()
    response = client.post(url, json_data, format='json')

    user_id_in_request = client.session.get('_auth_user_id')
    assert isinstance(client.session, SessionStore)
    assert 'Invalid Credentials' not in response.content.decode()
    assert response.status_code == 200, f"Error de solicitud: {response.content}"
    assert user.id == int(user_id_in_request)


@pytest.mark.django_db
def test_an_non_existing_user_cannot_login():

    json_data = {
        "username": 'fake@test.co',
        "password": 'user123456'
    }

    url = reverse('login')
    client = APIClient()
    response = client.post(url, json_data, format='json')

    assert 'A user with this email was not found.' in response.content.decode()
    assert response.status_code == 400, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_a_logged_without_email_fail_authentication():
    team = TeamFactory.create()
    user = CustomUser.objects.create_user(
        email='login@test.co',
        password='user123456',
        nick_name='nick',
        team=team)
    json_data = {
        "username": "",
        "password": 'user123456'
    }

    url = reverse('login')
    client = APIClient()
    response = client.post(url, json_data, format='json')

    assert 'This field may not be blank.' in response.content.decode()
    assert response.status_code == 400, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_a_logged_without_password_fail_authentication():
    team = TeamFactory.create()
    user = CustomUser.objects.create_user(
        email='login@test.co',
        password='user123456',
        nick_name='nick',
        team=team)
    json_data = {
        "username": user.email,
        "password": ''
    }

    url = reverse('login')
    client = APIClient()
    response = client.post(url, json_data, format='json')

    assert 'This field may not be blank.' in response.content.decode()
    assert response.status_code == 400, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_a_logged_with_invalid_password():
    team = TeamFactory.create()
    user = CustomUser.objects.create_user(
        email='login@test.co',
        password='user123456',
        nick_name='nick',
        team=team)
    json_data = {
        "username": user.email,
        "password": 'invalidpass'
    }

    url = reverse('login')
    client = APIClient()
    response = client.post(url, json_data, format='json')

    assert 'Invalid Credentials' in response.content.decode()
    assert response.status_code == 400, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_get_request_in_login():
    team = TeamFactory.create()
    user = CustomUser.objects.create_user(
        email='login@test.co',
        password='user123456',
        nick_name='nick',
        team=team)
    json_data = {
        "username": "",
        "password": 'user123456'
    }

    url = reverse('login')
    client = APIClient()
    response = client.get(url)

    assert 'Method \\"GET\\" not allowed.' in response.content.decode()
    assert response.status_code == 405, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_put_request_in_login():
    team = TeamFactory.create()
    user = CustomUser.objects.create_user(
        email='login@test.co',
        password='user123456',
        nick_name='nick',
        team=team)
    json_data = {
        "username": "",
        "password": 'user123456'
    }

    url = reverse('login')
    client = APIClient()
    response = client.put(url)

    assert 'Method \\"PUT\\" not allowed.' in response.content.decode()
    assert response.status_code == 405, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_delete_request_in_login():
    team = TeamFactory.create()
    user = CustomUser.objects.create_user(
        email='login@test.co',
        password='user123456',
        nick_name='nick',
        team=team)
    json_data = {
        "username": "",
        "password": 'user123456'
    }

    url = reverse('login')
    client = APIClient()
    response = client.delete(url)

    assert 'Method \\"DELETE\\" not allowed.' in response.content.decode()
    assert response.status_code == 405, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_logout_successfully_with_post_method(user_one):

    client = APIClient()
    client.force_authenticate(user=user_one)

    url = reverse('logout')
    response = client.post(url)

    session_id = response.cookies.get('sessionid')

    assert response.status_code == 200
    assert session_id is None


@pytest.mark.django_db
def test_logout_with_get_method(user_one):

    client = APIClient()
    client.force_authenticate(user=user_one)

    url = reverse('logout')
    response = client.get(url)

    session_id = response.cookies.get('sessionid')

    assert response.status_code == 405, f"Error de solicitud: {response.content}"
    assert 'Method \\"GET\\" not allowed.' in response.content.decode()


@pytest.mark.django_db
def test_unauthenticated_user_can_signup_successfully():
    TeamFactory.create(id=1)
    json_data = {
        'email': 'user@test.co',
        'nick_name': 'test',
        'password': 'passtest'
    }

    client = APIClient(9)
    url = reverse('signup')
    response = client.post(url, json_data, format='json')

    assert response.status_code == 201, f"Error de solicitud: {response.content}"


@pytest.mark.django_db
def test_authenticated_user_cannot_signup(user_one):
    TeamFactory.create(id=1)
    json_data = {
        'email': user_one.email,
        'nick_name': user_one.nick_name,
        'password': "test123456"
    }

    client = APIClient(9)
    url = reverse('signup')
    response = client.post(url, json_data, format='json')

    assert response.status_code == 400, f"Error de solicitud: {response.content}"
    assert "custom user with this email address already exists." in response.content.decode()


@pytest.mark.django_db
def test_unauthenticated_user_cannot_signup_with_missing_data():
    TeamFactory.create(id=1)
    json_data = {
        'email': 'usertest@test.co',
        'nick_name': 'test',
    }

    client = APIClient(9)
    url = reverse('signup')
    response = client.post(url, json_data, format='json')

    assert response.status_code == 400, f"Error de solicitud: {response.content}"
    assert "This field is required." in response.content.decode()


@pytest.mark.django_db
def test_unauthenticated_user_cannot_signup_with_an_exist_email(user_one):
    TeamFactory.create(id=1)
    json_data = {
        'email': user_one.email,
        'nick_name': 'test',
        'password': "test123456"
    }

    client = APIClient(9)
    url = reverse('signup')
    response = client.post(url, json_data, format='json')

    assert response.status_code == 400, f"Error de solicitud: {response.content}"
    assert "custom user with this email address already exists." in response.content.decode()
