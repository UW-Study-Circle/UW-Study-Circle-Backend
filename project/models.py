# models.py

from flask_login import UserMixin
from server import db, app
import jwt
from time import time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    gender = db.Column(db.Enum('MALE','FEMALE', 'OTHER')
    bday = db.Column(db.Date)
    phonenumber = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(1000))

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

