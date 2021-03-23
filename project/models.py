# models.py

from flask_login import UserMixin
from server import db, app
import jwt
from time import time
from marshmallow import Schema, fields

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
<<<<<<< HEAD
<<<<<<< HEAD
    gender = db.Column(db.String(1000))
    bday = db.Column(db.String(1000))
=======
    gender = db.Column(db.Enum('MALE','FEMALE', 'OTHER')
    birthday = db.Column(db.DateTime)
>>>>>>> e3e965d (Updated models.py)
    phonenumber = db.Column(db.String(100), nullable=True)

class Group(UserMixin, db.Model):
    groupname = db.Column(db.String(1000), unique=True)
    groupid = db.Column(db.Integer, primary_key=True)
    courseinfo = db.Column(db.String(1000))
    level = db.Column(db.String(1000))
    description = db.Column(db.String(2000), nullable=True)
    capacity = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    status = db.Column(db.String(100))

class Group(UserMixin, db.Model):
    groupname = db.Column(db.String(1000))
    groupid = db.Column(db.Integer, primary_key=True)
    courseInfo = db.Column(db.String(1000))
    level = db.Column(db.Enum('Beginner','Intermediate', 'Advanced')
    description = db.Column(db.String(2000))
    capacity = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    groupStatus = db.Column(db.Enum('Public','Private')
    def get_reset_token(self, expires=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires},
                          app.config['SECRET_KEY'],
                          algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, 
                                 app.config['SECRET_KEY'], 
                                algorithms='HS256')['reset_password']
        except Exception as e:
            print(e)
            return
        return User.query.get(user_id)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    firstname = fields.Str()
    lastname = fields.Str()
    gender = fields.Str()
    bday = fields.Str()
    formatted_name = fields.Method("format_name", dump_only=True)
    phonenumber = fields.Str()
    def format_name(self, user):
        return "{}".format(user.username)

class GroupSchema(Schema):
    groupname = fields.Str()
    groupid = fields.Int(dump_only=True)
    courseinfo = fields.Str()
    level = fields.Str()
    description = fields.Str()
    capacity = fields.Int()
    duration = fields.Int()
    status = fields.Str()
    def format_name(self, group):
        return "{}".format(group.groupname)
=======
    gender = db.Column(db.Enum('MALE','FEMALE', 'OTHER')
    birthday = db.Column(db.Date)
    phonenumber = db.Column(db.String(100), nullable=True)
>>>>>>> d62a3bf (Updated signup for main, init.py, models.py)
