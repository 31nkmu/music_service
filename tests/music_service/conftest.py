import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


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
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def activate(user, client):
    return client.get(f"/api/v1/account/activate/{user.activation_code}/")


@pytest.fixture
def token(client, activate):
    response = client.post('/api/v1/account/login/', dict(email='karimovbillal20002@gmail.com', password='123456'))
    # return {'Authorization': f"Bearer {response.data['access']}"}
    return str(response.data['access'])
