from flask import Response, request, jsonify
from flask_restful import Resource

from models import User, UserSchema
user_schema = UserSchema()

class HelloAPI(Resource):
    def get(self):
        # Add logic to find the user using username/email
        return {'hello': 'world'}

class UserAPI(Resource):
    def get(self, email):
        user = User.query.filter_by(email=email).first()
        result = jsonify(user_schema.dump(user))
        print(type(result))
        # Add logic to find the user using username/email
        return result