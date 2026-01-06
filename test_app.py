import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200

def test_get_user_found(client):
    response = client.get('/users/1')
    assert response.status_code == 200

def test_get_user_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == 404
    assert b'Not Found' in response.data

def test_create_user_success(client):
    response = client.post('/users', json={'name': 'Test', 'email': 'test@example.com'})
    assert response.status_code == 201

def test_create_user_bad_request(client):
    response = client.post('/users', json={'name': 'Test'})
    assert response.status_code == 400
    assert b'Bad Request' in response.data

def test_internal_server_error(client):
    response = client.get('/error')
    assert response.status_code == 500
    assert b'Internal Server Error' in response.data