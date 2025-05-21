import pytest
from app import create_app, db
from app.models import Book

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    with app.app_context():
        db.drop_all()  
        db.create_all()  
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()



def test_get_books_empty(client):

    response = client.get('/books', headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert len(data) == 0

def test_get_books_with_data(client):
    client.post('/books', json={'title': 'Test Book', 'author': 'Jane Doe'})

    response = client.get('/books', headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Test Book'

def test_reserve_book_success(client):
    with client.application.app_context():
        book = Book(title='Test Book', author='Author')
        db.session.add(book)
        db.session.commit()
        book_id = book.id
    response = client.post('/reservations', json={'book_id': book_id})
    assert response.status_code == 200
    assert response.json['message'] == 'Book reserved'
    assert response.json['book']['reserved'] is True

def test_reserve_nonexistent_book(client):
    response = client.post('/reservations', json={'book_id': 999})
    assert response.status_code == 404
    assert response.json['message'] == 'Book not found'

def test_reserve_already_reserved_book(client):
    with client.application.app_context():
        book = Book(title='Test Book', author='Author', reserved=True)
        db.session.add(book)
        db.session.commit()
        book_id = book.id
    response = client.post('/reservations', json={'book_id': book_id})
    assert response.status_code == 400
    assert response.json['message'] == 'Book already reserved'