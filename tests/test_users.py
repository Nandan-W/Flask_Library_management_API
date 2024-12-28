import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert response.get_json() == []

    user = User(username='Test User', password='password')
    db.session.add(user)    
    db.session.commit()

    response = client.get('/api/users')
    assert response.status_code == 200
    assert response.get_json() == [{'id': 1, 'username': 'Test User'}]

# added authorization here as it is necessary to add 
# new users without registration by admins
def test_add_user(client):
    client.post('/api/auth/register', json={
        'username': 'admin',
        'password': 'admin'
    })

    auth_response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin'
    })

    token = auth_response.json['access_token']

    response = client.post('/api/users', json={
        'username': 'Test User',
        'password': 'password'
    }, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 201
    assert response.get_json()['username'] == 'Test User'