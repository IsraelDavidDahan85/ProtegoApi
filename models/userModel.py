from datetime import datetime

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import Hyperlinks, URLFor
from flask_sqlalchemy import SQLAlchemy
import jwt
import utils.Cryptographer as Cryptographer

db = SQLAlchemy()
ma = Marshmallow()


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    salt = db.Column(db.String(100))

    def __init__(self, **data):
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.token = data.get('token', None)
        self.salt = data.get('salt', None)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password
        }

    def generate_token(self):
        self.token = jwt.encode({'id': self.id, 'email': self.email, 'date': str(datetime.now)},
                                'secret', algorithm='HS256')
        db.session.commit()
        return self.token

    def get_all_users(self, limit: int, offset: int):
        return self.query.limit(limit).offset(offset).all()

    def get_user_by_id(self, user_id: int):
        return self.query.filter_by(id=user_id).first()

    def get_user_by_email(self, email: str):
        return self.query.filter_by(email=email).first()

    def create_user(self):
        has_user_exist = self.get_user_by_email(self.email)
        if has_user_exist:
            return False, 'User already exists'
        self.password, self.salt = Cryptographer.encrypt(self.password)
        db.session.add(self)
        db.session.commit()
        return self, None

    def update_user(self, **new_user):
        if 'email' in new_user:
            user = self.get_user_by_email(new_user['email'])
            if user and user.id != self.id:
                return False, 'This email is already taken'

        for key, value in new_user.items():
            if key == 'password' and value is not None:
                self.password, self.salt = Cryptographer.encrypt(value)
            elif value is None:
                continue
            else:
                setattr(self, key, value)
        db.session.commit()
        return self, None

    def delete_user(self, user_id: int):
        user = db.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return user

    def get_decrypted_password(self):
        return Cryptographer.decrypt(self.password, self.salt)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        fields = ("id", "first_name", "last_name", "email")

    _links = Hyperlinks(
        {"self": URLFor("user", values=dict(id="<id>"))}
    )


user_schema = UserSchema()
users_schema = UserSchema(many=True)
