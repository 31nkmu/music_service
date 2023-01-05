import pytest


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
def test_activate(activate):
    msg = activate
    assert msg.data == {'msg': 'ваш аккаунт успешно активирован'}


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
    a = client.post(path=f'/api/v1/account/change_password/', data=data, **headers)
    print(a.status_code)
    response = client.post('/api/v1/account/login/', dict(email='karimovbillal20002@gmail.com', password='123456'))
    assert response.status_code == 401
