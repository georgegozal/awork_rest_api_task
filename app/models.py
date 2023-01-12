from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .extensions import ma


class Base:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def update(cls, id, **kwargs):
        cls.query.filter_by(id=id).update(kwargs)
        db.session.commit()


# Product Class/Model
class User(db.Model, Base):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    addresses = db.relationship('Address', backref='user', lazy=True)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    # password
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Address(db.Model, Base):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    street = db.Column(db.String(120))
    zip_code = db.Column(db.String(120), nullable=False)

    @classmethod
    def update_address(self,  **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            db.session.add(self)
            db.session.commit()


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'first_name', 'last_name')


# Init schema
user_schema = UserSchema()

users_schema = UserSchema(many=True)


class AddressSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'country', 'city', 'street', 'zip_code')


address_schema = AddressSchema()

address_schemas = AddressSchema(many=True)
