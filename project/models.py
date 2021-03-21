# models.py

from flask_login import UserMixin
from server import db, app
import jwt
from time import time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

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

