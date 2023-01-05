import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


def get_user():
    return User.objects.get(
        email='karimovbillal20002@gmail.com',
    )


@pytest.fixture
def user():
    user = User.objects.create_user(
        email='karimovbillal20002@gmail.com',
        password='123456',
        card_number='4169000000000000',
        card_balance=5000,
        gender='m',
        is_subscribed=True
    )
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def activate(user, client):
    user = get_user()
    response = client.get(f"/api/v1/account/activate/{user.activation_code}/")
    return response


@pytest.fixture
def token(client, activate):
    response = client.post('/api/v1/account/login/', dict(email='karimovbillal20002@gmail.com', password='123456'))
    return str(response.data['access'])


@pytest.fixture
def album(client, token):
    album = dict(title='Newalbum', singer='Jony', owner=token)
    headers = {
        'HTTP_AUTHORIZATION': 'Bearer ' + token,
    }
    response = client.post(path='/api/v1/product/album/', data=album, **headers)
    return response.data