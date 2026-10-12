def test_openaip_available(client):
    response = client.get('/openapi.json')

    assert response.status_code == 200
    assert response.json()['info']['title'] == 'FastAPI'

def test_projects_require_auth(client):
    response = client.get('/projects')
    assert response.status_code == 401

def test_register_login_and_get_all_projects(client):
    register = client.post(
        '/auth/register',
        json={'email': 'mail@gmail.com', 'password': 'qwerty1234'}
    )
    assert register.status_code == 201

    login = client.post(
        '/auth/login',
        json={'email': 'mail@gmail.com', 'password': 'qwerty1234'}
    )
    assert login.status_code == 200
    token = login.json()['access_token']

    projects = client.get(
        '/projects',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert projects.status_code == 200
    assert projects.json() == []
