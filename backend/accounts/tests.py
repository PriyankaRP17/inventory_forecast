import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(username='testuser', password='testpass123', role='staff'):
        return User.objects.create_user(
            username=username,
            password=password,
            role=role
        )
    return make_user


@pytest.mark.django_db
def test_register_user(api_client):
    payload = {
        'username': 'priyanka',
        'email': 'priyanka@test.com',
        'password': 'testpass123',
        'role': 'staff'
    }
    response = api_client.post('/api/auth/register/', payload)
    assert response.status_code == 201
    assert 'access' in response.data
    assert response.data['user']['username'] == 'priyanka'


@pytest.mark.django_db
def test_login_user(api_client, create_user):
    create_user(username='priyanka', password='testpass123')
    payload = {'username': 'priyanka', 'password': 'testpass123'}
    response = api_client.post('/api/auth/login/', payload)
    assert response.status_code == 200
    assert 'access' in response.data


@pytest.mark.django_db
def test_login_wrong_password(api_client, create_user):
    create_user(username='priyanka', password='testpass123')
    payload = {'username': 'priyanka', 'password': 'wrongpass'}
    response = api_client.post('/api/auth/login/', payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_staff_cannot_access_admin_endpoint(api_client, create_user):
    user = create_user(username='staffuser', role='staff')
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/auth/me/')
    assert response.status_code == 200
    assert response.data['role'] == 'staff'


@pytest.mark.django_db
def test_me_endpoint_requires_auth(api_client):
    response = api_client.get('/api/auth/me/')
    assert response.status_code == 401
