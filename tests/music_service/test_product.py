import pytest


@pytest.mark.django_db
def test_create_album(client, token):
    data = dict(title='Newalbum', singer='Jony', owner=token)
    headers = {
        'HTTP_AUTHORIZATION': 'Bearer ' + token,
    }
    response = client.post(path='/api/v1/product/album/', data=data, **headers)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_music(client, album, token):
    i = open('Screenshot_from_2022-12-21_20-35-26.png', 'rb')
    m = open('V__x_v_PrInce_-_Мурашки.mp3', 'rb')
    data = dict(title='DanzaKuduro', singer='Jony', album=album['title'],  image=i, music=m, owner=token)
    headers = {
        'HTTP_AUTHORIZATION': 'Bearer ' + token,
    }
    response = client.post(path='/api/v1/product/', data=data, **headers)
    i.close()
    m.close()
    assert response.status_code == 201
