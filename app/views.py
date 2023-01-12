from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,\
    jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User, user_schema, users_schema


bp = Blueprint('bp', __name__)


# Register User
@bp.route('/user', methods=['POST'])
def sign_up():
    email = request.json['email']
    password = request.json['password']
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    new_user = User(email, password, first_name, last_name)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Log In
@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad email or password"}), 401


# Get Logined user email
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


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


# Delete User
@bp.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
