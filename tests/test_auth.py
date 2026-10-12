def test_register_duplicate_email_409(client):
    payload = {'email': 'name@gmail.com', 'password': 'qwerty123'}
    client.post('/auth/register', json=payload)

    response = client.post('/auth/register', json=payload)

    assert response.status_code == 409


def test_login_wrong_password(client):
    payload = {'email': 'name@gmail.com', 'password': 'qwerty123'}
    client.post('/auth/register', json=payload)

    response = client.post(
        '/auth/login',
        json={'email': payload['email'], 'password': 'qwerty1234'}
    )

    assert response.status_code == 401
