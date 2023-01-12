from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity




db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
jwt = JWTManager()
