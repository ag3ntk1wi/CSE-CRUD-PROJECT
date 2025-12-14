import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

def get_token(client):
    response = client.post('/login', json={
        "username": "admin",
        "password": "admin123"
    })
    return response.get_json()['access_token']


def test_get_students(client):
    token = get_token(client)

    response = client.get(
        '/students',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200


def test_create_student(client):
    token = get_token(client)

    response = client.post(
        '/students',
        json={
            "last_name": "Test",
            "first_name": "User",
            "age": "20",
            "block": "1",
            "year": "2",
            "instructor_id": 1,
            "program_id": 1
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 201

def test_create_student_empty_body(client):
    token = get_token(client)

    response = client.post(
        '/students',
        json={},
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400

def test_update_nonexistent_student(client):
    token = get_token(client)

    response = client.put(
        '/students/9999',
        json={
            "age": "22",
            "block": "1",
            "year": "3"
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404

def test_delete_nonexistent_student(client):
    token = get_token(client)

    response = client.delete(
        '/students/9999',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404

def test_search_missing_param(client):
    token = get_token(client)

    response = client.get(
        '/students/search',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
