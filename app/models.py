from .extensions import db


# Product Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


# Product Schema

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'first_name', 'last_name')


# Init schema
user_schema = UserSchema()

users_schema = UserSchema(many=True)
