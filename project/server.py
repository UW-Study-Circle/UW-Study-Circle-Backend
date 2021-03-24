# init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_mail import Mail
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
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

# app.config['APISPEC_SPEC'] =  APISpec(
#         title='Awesome Project',
#         version='v1',
#         plugins=[MarshmallowPlugin()],
#         openapi_version='2.0.0'
#     )
# app.config['APISPEC_SWAGGER_URL'] = '/swagger/',  # URI to access API Doc JSON 
# app.config['APISPEC_SWAGGER_UI_URL'] = '/swagger-ui/'  # URI to access UI of API Doc
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

docs = FlaskApiSpec(app)
api = Api(app)
api.add_resource(HelloAPI, '/', endpoint="helloapi")
docs.register(HelloAPI)

api.add_resource(UserAPI, '/api/user/', endpoint="create_user", methods=['POST'])
api.add_resource(UserAPI, '/api/user/email/<email>', endpoint="search_user", methods=['GET'])
api.add_resource(UserAPI, '/api/user/id/<id>', endpoint="delete_user", methods=['DELETE'])

docs.register(UserAPI, endpoint="create_user")
docs.register(UserAPI, endpoint="search_user")
docs.register(UserAPI, endpoint="delete_user")