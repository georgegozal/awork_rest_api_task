from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, user_schema


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
