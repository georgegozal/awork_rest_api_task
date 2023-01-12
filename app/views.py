from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,\
    jwt_required, get_jwt_identity
from app.models import User, user_schema, users_schema,\
    Address, address_schema, address_schemas


bp = Blueprint('bp', __name__)


# Register User
@bp.route('/user', methods=['POST'])
def sign_up():
    email = request.json['email']
    password = request.json['password']
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    new_user = User(email, password, first_name, last_name)

    new_user.save()

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
    all_users = User.get_all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# Get Single User
@bp.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)


# Update User
@bp.route('/user/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.update(id, **data)
    return user_schema.jsonify(user)


# Delete User
@bp.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    user.delete()
    return user_schema.jsonify(user)


@bp.route('/address', methods=['POST'])
@jwt_required()
def add_address():

    current_user = get_jwt_identity()
    user_id = User.query.filter_by(email=current_user).first().id
    address = Address.query.filter_by(user_id=user_id).first()
    if not address:
        country = request.json['country']
        city = request.json['city']
        street = request.json['street']
        zip_code = request.json['zip_code']

        new_address = Address(
            user_id=user_id,
            country=country,
            city=city,
            street=street,
            zip_code=zip_code
        )

        new_address.save()
    else:
        return jsonify({"msg": "Address for current user already exists"}), 400
    # return new address
    return address_schema.jsonify(new_address)


@bp.route('/address/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    data = request.get_json()
    address = Address.query.get_or_404(id)
    address.update(id, **data)
    # return updated address
    return address_schema.jsonify(address)


@bp.route('/address/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    address = Address.query.get_or_404(id)
    address.delete()
    # Return deleted address
    return address_schema.jsonify(address)


@bp.route('/address', methods=['GET'])
@jwt_required()
def list_addresses():
    all_addresses = Address.get_all()
    result = address_schemas.dump(all_addresses)
    return jsonify(result)
