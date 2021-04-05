# init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_mail import Mail
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_login import LoginManager 
from flask_cors import CORS
import os



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='UW Study-Circle',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

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
from models import User, Group

with app.app_context():
    db.create_all()
    
login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

from api import *

docs = FlaskApiSpec(app)
api = Api(app)
CORS(app, supports_credentials=True)
api.add_resource(ProfileAPI, '/', endpoint="profile", methods=['GET'])
api.add_resource(ProfileAPI, '/id/<id>', endpoint="profile_id", methods=['GET'])
api.add_resource(ProfileAPI, '/api/logout/<logout>', endpoint="logout", methods=['GET'])

api.add_resource(ProfileAPI, '/api/login/', endpoint="login_user", methods=['POST'])

docs.register(ProfileAPI, endpoint="profile")
docs.register(ProfileAPI, endpoint="profile_id")
docs.register(ProfileAPI, endpoint="login_user")
docs.register(ProfileAPI, endpoint="logout")



api.add_resource(UserAPI, '/api/user/', endpoint="create_user", methods=['POST'])
api.add_resource(UserAPI, '/api/user/email/<email>/password/<password>', endpoint="search_user", methods=['GET'])
api.add_resource(UserAPI, '/api/user/id/<id>', endpoint="delete_user", methods=['DELETE'])

docs.register(UserAPI, endpoint="create_user")
docs.register(UserAPI, endpoint="search_user")
docs.register(UserAPI, endpoint="delete_user")

api.add_resource(GroupAPI, '/api/group/', endpoint="create_group", methods=['POST'])
api.add_resource(GroupAPI, '/api/group/', endpoint="search_group", methods=['GET'])
api.add_resource(GroupAPI, '/api/group/<id>', endpoint="get_group_id", methods=['GET'])
api.add_resource(GroupAPI, '/api/group/<search>', endpoint="search_group_query", methods=['GET'])
api.add_resource(GroupAPI, '/api/group/id/<id>', endpoint="delete_group", methods=['DELETE'])

docs.register(GroupAPI, endpoint="create_group")
docs.register(GroupAPI, endpoint="search_group")
docs.register(GroupAPI, endpoint="get_group_id")
docs.register(GroupAPI, endpoint="search_group_query")
docs.register(GroupAPI, endpoint="delete_group")