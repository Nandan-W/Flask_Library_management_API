import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()



@pytest.fixture
def client(app):
    return app.test_client()


def test_register_user(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })


    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'



def test_register_duplicate_user(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    assert response.status_code == 400
    assert response.json['error'] == 'Username already exists'



def test_login_user(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert response.json['error'] == 'Invalid credentials'