# init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from datetime import timedelta
from flask_mail import Mail
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
    

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)

