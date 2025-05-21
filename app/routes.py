from flask import Blueprint, jsonify, request, render_template
from .models import Book
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/add-book')
def add_book_page():
    return render_template('add_book.html')

@bp.route('/books', methods=['GET'])
def get_books():
    books = db.session.execute(db.select(Book)).scalars().all()
    if request.accept_mimetypes['application/json']:
        return jsonify([book.to_dict() for book in books])
    return render_template('books.html', books=books)

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.form if not request.is_json else request.get_json()
    if not data or 'title' not in data or 'author' not in data:
        if request.is_json:
            return jsonify({'message': 'Missing title or author'}), 400
        return render_template('add_book.html', error='Missing title or author')

    title = data['title']
    author = data['author']
    existing_book = db.session.execute(
        db.select(Book).filter_by(title=title, author=author)
    ).scalar_one_or_none()
    if existing_book:
        if request.is_json:
            return jsonify({'message': 'Book already exists'}), 400
        return render_template('add_book.html', error='Book already exists')

    new_book = Book(title=title, author=author)
    db.session.add(new_book)
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'Book added successfully', 'book': new_book.to_dict()}), 201
    return render_template('book_added.html', book=new_book)

@bp.route('/reservations', methods=['POST'])
def reserve_book():
    data = request.form if not request.is_json else request.get_json()
    book_id = data.get('book_id')
    book = db.session.get(Book, book_id)
    if not book:
        if request.is_json:
            return jsonify({'message': 'Book not found'}), 404
        return render_template('reservation_result.html', error='Book not found')
    if book.reserved:
        if request.is_json:
            return jsonify({'message': 'Book already reserved'}), 400
        return render_template('reservation_result.html', error='Book is already reserved')

    book.reserved = True
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'Book reserved', 'book': book.to_dict()})
    return render_template('reservation_result.html', book=book)

@bp.route('/books', methods=['GET'])
def api_get_books():
    books = db.session.execute(db.select(Book)).scalars().all()
    return jsonify([book.to_dict() for book in books])

@bp.route('/books/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify(book.to_dict())

@bp.route('/reservations', methods=['POST'])
def api_reserve_book():
    data = request.get_json()
    book_id = data.get('book_id')
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    if book.reserved:
        return jsonify({'message': 'Book already reserved'}), 400
    book.reserved = True
    db.session.commit()
    return jsonify({'message': 'Book reserved', 'book': book.to_dict()})