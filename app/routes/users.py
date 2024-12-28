from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

bp = Blueprent('auth' , __name__)

@bp.route('/api/users' , methods ['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict()  for user in users ]) , 200


@bp.route('/api/users' , methods = ['POST'] )
@jwt_required()
def add_user():
    data = request.get_json()
    
    new_user=User(
        username=data['username'],
        password=data['password'],
    )

    db.session.add(new_user)
    db.session.commit(new_user)

    return jsonify({'message': 'User created successfully'}), 201



@bp.route('/api/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.username = data['username']
    user.password = data['password']
    
    db.session.commit()
    
    return jsonify(user.to_dict()) , 200



@bp.route('/api/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 204