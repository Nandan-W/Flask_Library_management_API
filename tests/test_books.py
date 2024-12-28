import pytest
from app import create_app, db
from app.models import Book, User

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

def test_get_books(client):
    response = client.get('/api/books')
    assert response.status_code == 200
    assert 'books' in response.json

def test_create_book(client):
    client.post('/api/auth/register', json={
        'username': 'test',
        'password': 'test'
    })
    
    auth_response = client.post('/api/auth/login', json={
        'username': 'test',
        'password': 'test'
    })
    
    token = auth_response.json['access_token']
    
    response = client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'quantity': 5,
            'published_date': '2000-01-01',
            'available': 5,
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 201
    assert response.json['title'] == 'Test Book'

def test_create_book_unauthorized(client):
    response = client.post('/api/books', json={
        'title': 'Unauthorized Book',
        'author': 'Unauthorized Author',
        'isbn': '0987654321',
        'quantity': 1,
        'published_date': '2023-01-01',
        'available': 1,
    })
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'

def test_create_book_incomplete_data(client):
    client.post('/api/auth/register', json={
        'username': 'test',
        'password': 'test'
    })
    
    auth_response = client.post('/api/auth/login', json={
        'username': 'test',
        'password': 'test'
    })
    
    token = auth_response.json['access_token']
    
    response = client.post('/api/books', json={
        'title': 'Incomplete Book',
        'author': 'Incomplete Author',
        # Missing 'isbn', 'quantity', 'published_date', 'available'
    },
    headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Missing required fields'

def test_update_book(client):
    client.post('/api/auth/register', json={
        'username': 'test',
        'password': 'test'
    })
    
    auth_response = client.post('/api/auth/login', json={
        'username': 'test',
        'password': 'test'
    })
    
    token = auth_response.json['access_token']
    
    client.post('/api/books', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '1234567890',
        'quantity': 5,
        'published_date': '2000-01-01',
        'available': 5,
    },
    headers={'Authorization': f'Bearer {token}'})
    
    response = client.put('/api/books/1', json={
        'title': 'Updated Book',
        'author': 'Updated Author',
        'isbn': '1234567890',
        'quantity': 10,
        'published_date': '2000-01-01',
        'available': 10,
    },
    headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Book'

def test_update_book_unauthorized(client):
    response = client.put('/api/books/1', json={
        'title': 'Unauthorized Update',
        'author': 'Unauthorized Author',
        'isbn': '0987654321',
        'quantity': 1,
        'published_date': '2023-01-01',
        'available': 1,
    })
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'

def test_delete_book(client):
    client.post('/api/auth/register', json={
        'username': 'test',
        'password': 'test'
    })
    
    auth_response = client.post('/api/auth/login', json={
        'username': 'test',
        'password': 'test'
    })
    
    token = auth_response.json['access_token']
    
    client.post('/api/books', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '1234567890',
        'quantity': 5,
        'published_date': '2000-01-01',
        'available': 5,
    },
    headers={'Authorization': f'Bearer {token}'})
    
    response = client.delete('/api/books/1', headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 204

def test_delete_book_unauthorized(client):
    response = client.delete('/api/books/1')
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'