from flask import Blueprint, jsonify, request
from .models import Book
from . import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': b.id, 'title': b.title, 'author': b.author, 'reserved': b.reserved} for b in books])

@bp.route('/reservations', methods=['POST'])
def reserve_book():
    data = request.get_json()
    book_id = data.get('book_id')
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    if book.reserved:
        return jsonify({'message': 'Book already reserved'}), 400
    book.reserved = True
    db.session.commit()
    return jsonify({'message': 'Book reserved', 'book': {'id': book.id, 'title': book.title, 'reserved': book.reserved}})