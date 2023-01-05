import pytest

from tests.music_service.conftest import get_user


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        email='karimovbillal20002@gmail.com',
        password='123456',
        password_repeat='123456',
        card_number='4169000000000000',
        card_balance=5000,
        gender='m',
        is_subscribed=True
    )

    response = client.post('/api/v1/account/register/', payload)
    data = response.data
    assert data['email'] == 'karimovbillal20002@gmail.com'
    assert data['card_number'] == '4169000000000000'
    assert data['card_balance'] == '5000.00'
    assert data['gender'] == 'm'
    assert data['is_subscribed'] == True
    assert 'password' not in data


@pytest.mark.django_db
def test_activate(client, activate):
    user = get_user()
    msg = activate
    assert msg.data == {'msg': 'ваш аккаунт успешно активирован'}
    assert user.is_active == True
    assert not user.activation_code


@pytest.mark.django_db
def test_login(client, activate):
    response = client.post('/api/v1/account/login/', dict(email='karimovbillal20002@gmail.com', password='123456'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail(client):
    response = client.post('/api/v1/account/login/', dict(email='karimovbillal20002@gmail.com', password='123456'))
    assert response.status_code == 401


@pytest.mark.django_db
def test_change_password(client, token):
    data = dict(old_password='123456', new_password='1234567', new_password_repeat='1234567')
    headers = {
        'HTTP_AUTHORIZATION': 'Bearer ' + token,
    }
    client.post(path=f'/api/v1/account/change_password/', data=data, **headers)
    response = client.post('/api/v1/account/login/', dict(email='karimovbillal20002@gmail.com', password='123456'))
    assert response.status_code == 401


@pytest.mark.django_db
def test_forgot_password(client, user, activate):
    data = dict(email=user.email)
    response = client.post('/api/v1/account/forgot_password/', data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_forgot_password_confirm(client, user):
    data = dict(email=user.email)
    old_password = user.password
    client.post('/api/v1/account/forgot_password/', data=data)
    user = get_user()
    code = user.activation_code
    data = dict(
        email=user.email,
        code=code,
        password='1234567',
        password_repeat='1234567'
    )
    response = client.post('/api/v1/account/forgot_password_confirm/', data=data)
    user = get_user()
    new_password = user.password
    login_response = client.post('/api/v1/account/login/', dict(email=user.email, password='1234567'))
    login_fail = client.post('/api/v1/account/login/', dict(email=user.email, password='123456'))
    assert response.status_code == 201
    assert not user.activation_code
    assert not old_password == new_password
    assert login_response.status_code == 200
    assert login_fail.status_code == 401
