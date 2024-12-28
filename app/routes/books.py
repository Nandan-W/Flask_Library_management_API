from flask import Blueprint, request, jsonify
from app.models import Book
from app import db
from flask_jwt_extended import jwt_required

bp = Blueprint('books', __name__)

@bp.route('/api/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')

    query = Book.query
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) | 
            (Book.author.ilike(f'%{search}%'))
        )

    pagination = query.paginate(page=page, per_page=per_page)
    books = pagination.items

    return jsonify({
        'books': [book.to_dict() for book in books],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@bp.route('/api/books', methods=['POST'])
@jwt_required()
def create_book():
    data = request.get_json()
    
    if not all(k in data for k in ('title', 'author', 'isbn', 'quantity')):
        return jsonify({'error': 'Missing required fields'}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        published_date=data['published_date'],
        quantity=data['quantity'],
        available=data['quantity'],
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify(new_book.to_dict()), 201


@bp.route('/api/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    data = request.get_json()
    book = Book.query.get(id)

    if not book:
        return jsonify({'message': 'Book not found'}) , 404

    book.title = data['title']
    book.author = data['author']
    book.published_date = data['published_date']
    book.isbn = data['isbn']
    book.quantity = data['quantity']
    book.available = data['available']

    db.session.commit()

    return jsonify(book.to_dict()) , 200


@bp.route('/api/books/<int:id>' , methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found'}) , 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'}), 204