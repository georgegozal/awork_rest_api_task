from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, user_schema, users_schema


bp = Blueprint('bp', __name__)


# Register User
@bp.route('/user', methods=['POST'])
def add_user():
    email = request.json['email']
    password = request.json['password']
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    new_user = User(email, password, first_name, last_name)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Get All Users
@bp.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# Get Single User
@bp.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Update User
@bp.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    email = request.json['email']
    password = request.json['password']
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    user.email = email
    user.password = password
    user.first_name = first_name
    user.last_name = last_name

    db.session.commit()

    return user_schema.jsonify(user)
