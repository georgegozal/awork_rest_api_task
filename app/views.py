from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,\
    jwt_required, get_jwt_identity
from app.models import User, user_schema, users_schema,\
    Address, address_schema, address_schemas


bp = Blueprint('bp', __name__)


# Register User
@bp.route('/user', methods=['POST'])
def sign_up():
    data = request.get_json()
    u = User.query.filter_by(email=data.get('email')).first()
    if u:
        return jsonify({"msg": "A user with this email already exists."}), 409
    new_user = User()
    new_user.create(**data)
    new_user.save()

    return user_schema.jsonify(new_user)


# Log In
@bp.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad email or password"}), 401


# add New address for Logged user
@bp.route('/address', methods=['POST'])
@jwt_required()
def add_address():

    current_user = get_jwt_identity()
    data = request.get_json()

    new_address = Address()
    new_address.create(
        user_id=current_user,
        **data
        )
    new_address.save()
    return address_schema.jsonify(new_address)


@bp.route('/address/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    data = request.get_json()
    current_user = get_jwt_identity()
    address = Address.query.get_or_404(id)
    if address.user_id != current_user:
        return jsonify(
            {"msg": "You are not allowed to update this address."}), 403
    else:
        address.update(id, **data)
        # return updated address
        return address_schema.jsonify(address)


# Delete User`s Address
@bp.route('/address/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    current_user = get_jwt_identity()
    address = Address.query.get_or_404(id)
    if address.user_id != current_user:
        return jsonify(
            {"msg": "You are not allowed to delete this address."}), 403
    else:
        address.delete()
        # Return deleted address
        return address_schema.jsonify(address)


# Get User`s Addresses
@bp.route('/address', methods=['GET'])
@jwt_required()
def list_addresses():
    current_user = get_jwt_identity()
    all_addresses = Address.query.filter_by(user_id=current_user).all()
    result = address_schemas.dump(all_addresses)
    return jsonify(result)
