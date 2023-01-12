from flask import Flask
from .config import Config
from .extensions import db, migrate, ma, jwt
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
