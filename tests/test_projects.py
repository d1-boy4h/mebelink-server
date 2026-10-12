from src.core import ProjectStatus

from .helpers import register_and_login


def test_create_project(client):
    headers = register_and_login(client, 'test@test.com', 'qwerty123')

    response = client.post(
        '/projects',
        json={'title': 'Новый проект'},
        headers=headers
    )

    body = response.json()
    assert response.status_code == 201
    assert body['title'] == 'Новый проект'
    assert body['status'] == ProjectStatus.NOT_IN_PROGRESS
    assert body['is_improvements'] == False
    assert body['end_date'] is None
    assert body['address'] is None
    assert body['phone'] is None

def test_user_cannot_see_other_users_projects(client):
    user_1 = register_and_login(client, 'user.1@test.com', 'qwerty123')
    response = client.post(
        '/projects',
        json={'title': 'Проект первого пользователя'},
        headers=user_1
    )

    user_2 = register_and_login(client, 'user.2@test.com', 'qwerty123')
    response = client.get('/projects', headers=user_2)

    assert response.status_code == 200
    assert response.json() == []
