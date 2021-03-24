# init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_mail import Mail
from flask_restful import Api
import os



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)


app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' 
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=1800)
app.config['MAIL_SERVER'] = 'smtp.126.com'#.office365.com'
app.config['MAIL_PORT'] = 465 #587
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'yyt_2008@126.com'#os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = '150724yan'#os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

db.init_app(app)
from models import User

with app.app_context():
    db.create_all()
    

from api import *

api = Api(app)
api.add_resource(HelloAPI, '/')
api.add_resource(UserAPI, '/api/user/', endpoint="create_user")
api.add_resource(UserAPI, '/api/user/email/<email>', endpoint="search_user")
api.add_resource(UserAPI, '/api/user/id/<id>', endpoint="delete_user")

