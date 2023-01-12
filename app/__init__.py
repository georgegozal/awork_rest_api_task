from flask import Flask, request, jsonify
from .config import Config
from .extensions import db, migrate, login_manager, ma, jwt
from .views import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(bp)
    register_extensions(app)
    return app


def register_extensions(app):

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-Marshmallow
    ma.init_app(app)

    # Setup Flask-JWT-Extended
    jwt.init_app(app)

    # Flask-Login
    @login_manager.user_loader
    def load_user(id_):
        return User.query.get(id_)

    login_manager.init_app(app)
