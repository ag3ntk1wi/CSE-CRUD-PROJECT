import pytest
from app import app

# ---------------- FIXTURES ----------------

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


# ---------------- AUTH TESTS ----------------

def test_login_success(client):
    response = client.post('/login', json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_invalid_credentials(client):
    response = client.post('/login', json={
        "username": "admin",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_access_without_token(client):
    response = client.get('/students')
    assert response.status_code == 401


# ---------------- READ TESTS ----------------

def test_get_students_json(client):
    token = get_token(client)

    response = client.get(
        '/students',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_students_xml(client):
    token = get_token(client)

    response = client.get(
        '/students?format=xml',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.content_type == 'application/xml'


# ---------------- CREATE TESTS ----------------

def test_create_student_success(client):
    token = get_token(client)

    response = client.post(
        '/students',
        json={
            "last_name": "Test",
            "first_name": "User",
            "age": 20,
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


def test_create_student_missing_fields(client):
    token = get_token(client)

    response = client.post(
        '/students',
        json={
            "last_name": "Test"
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400


# ---------------- UPDATE TESTS ----------------

def test_update_nonexistent_student(client):
    token = get_token(client)

    response = client.put(
        '/students/9999',
        json={
            "age": 22,
            "block": "1",
            "year": "3"
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404


def test_update_student_success(client):
    token = get_token(client)

    # Create a student first
    create_response = client.post(
        '/students',
        json={
            "last_name": "Update",
            "first_name": "Test",
            "age": 20,
            "block": "1",
            "year": "2",
            "instructor_id": 1,
            "program_id": 1
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert create_response.status_code == 201

    # Get created student's ID
    students = client.get(
        '/students',
        headers={'Authorization': f'Bearer {token}'}
    ).get_json()

    student_id = students[-1]['id']

    # Update that student
    update_response = client.put(
        f'/students/{student_id}',
        json={
            "age": 21,
            "block": "2",
            "year": "3"
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert update_response.status_code == 200



# ---------------- DELETE TESTS ----------------

def test_delete_nonexistent_student(client):
    token = get_token(client)

    response = client.delete(
        '/students/9999',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404


def test_delete_student_success(client):
    token = get_token(client)

    # Create a student first
    create_response = client.post(
        '/students',
        json={
            "last_name": "Delete",
            "first_name": "Me",
            "age": 19,
            "block": "1",
            "year": "1",
            "instructor_id": 1,
            "program_id": 1
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert create_response.status_code == 201

    # Fetch students and get the last inserted ID
    students = client.get(
        '/students',
        headers={'Authorization': f'Bearer {token}'}
    ).get_json()

    student_id = students[-1]['id']

    # Delete that student
    delete_response = client.delete(
        f'/students/{student_id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert delete_response.status_code == 200



# ---------------- SEARCH TESTS ----------------

def test_search_missing_param(client):
    token = get_token(client)

    response = client.get(
        '/students/search',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400


def test_search_student_success(client):
    token = get_token(client)

    response = client.get(
        '/students/search?name=Test',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
