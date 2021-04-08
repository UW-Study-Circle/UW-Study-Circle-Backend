# models.py

from flask_login import UserMixin
from server import db, app
import jwt
from time import time
from flask_sqlalchemy import SQLAlchemy

group_user = db.Table('group_user', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    gender = db.Column(db.String(1000))
    bday = db.Column(db.String(1000))
    phonenumber = db.Column(db.String(100), nullable=True)
    
    groups = db.relationship('Group', secondary=group_user, 
        backref=db.backref('user_id', lazy='dynamic'))
    
    def __repr__(self):
        return "<Users id='%s' username='%s'>" % (self.id, self.username)

    def get_token(self, expires=600):
        return jwt.encode({'email_link': self.id, 'exp': time() + expires},
                          app.config['SECRET_KEY'],
                          algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            user_id = jwt.decode(token, 
                                 app.config['SECRET_KEY'], 
                                algorithms='HS256')['email_link']
        except Exception as e:
            print(e)
            return
        return User.query.get(user_id)
    
    
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    # chatroom_id = db.Column(db.Integer, ForeignKey("chatroom.id"))
    share_link = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Interval, nullable=True)
    group_name = db.Column(db.String(100), unique=True)
    course_num = db.Column(db.String(100))
    capacity = db.Column(db.Integer, default = 50)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    description = db.Column(db.Text)
    status = db.Column(db.String(10))
    created_time = db.Column(db.DateTime, default=db.func.now())
    
    users = db.relationship('User', secondary=group_user,
        backref=db.backref('group_id', lazy='dynamic'))
    
    def __repr__(self):
        return "<Groups id='%s' group_name='%s'>" % (self.id, self.group_name)

