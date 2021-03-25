from flask import Response, request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_apispec import doc, use_kwargs, marshal_with
from flask_apispec.views import MethodResource

from models import User, UserSchema
user_schema = UserSchema()

from flask_login import login_user, logout_user, login_required, current_user

class ProfileAPI(MethodResource, Resource):
    @doc(description='User Profile API.', tags=['User-Profile'])
    def get(self):
        '''
        Get method to fetch logged-in user's profile
        '''
        if current_user.is_authenticated:
            print(current_user)
            return user_schema.dump(current_user)
        return {'Error': 'Unauthenticated'}

class UserAPI(MethodResource, Resource):
    @doc(description='Post request for signup feature.', tags=['User'])
    @use_kwargs(UserSchema)
    # @marshal_with(UserSchema, code=201)
    def post(self, **kwargs):
        '''
        Post method for User Signup
        '''
        body = request.get_json()
        if body is None:
            return jsonify({"Error": "Data not in correct format"})
        print(body)
        
        result = dict()
        try:
            username = body["username"]
            password = body["password"]
            email = body["email"]
            firstname = body["firstname"]
            lastname = body["lastname"]
            gender = body["gender"]
            bday = body["bday"]
            phone = body["phonenumber"]         

            # Check if a user exists with the give username/email
            email_exist = User.query.filter_by(email=email).first() 
            name_exist = User.query.filter_by(username=username).first() 
            if email_exist:
                result["Duplicate"] = "Email already exists"
                return jsonify(result)
            if name_exist:
                result["Duplicate"] = "Name already exists"
                return jsonify(result)   
            new_user = User(
                email=email, username=username, password=generate_password_hash(password, method='sha256'),
                lastname=lastname, firstname=firstname, gender=gender, bday=bday, phonenumber=phone)
            # add the new user to the database
            from server import db

            db.session.add(new_user)
            db.session.commit()
            result["Success"] = "User created"
            return jsonify(result)
            

        except Exception as e:
            error = dict()
            error["Error"] = str(e)
            return jsonify(error)

    @doc(description='Get request for login feature.', tags=['User'])
    def get(self, email, password):
        '''
        Get method for User Login
        '''
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password): 
            return {"Content": None} # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=True)
        result = dict()
            
        result["Content"] = user_schema.dump(user)
        # print(type(result))
        return jsonify(result)

    @login_required
    @doc(description='Delete request for delete account feature.', tags=['User'])
    def delete(self, id):
        '''
        Delete method for User deletion
        '''
        current_id = current_user.id

        if int(id) != current_id:
            return jsonify({"Error": "Incorrect User ID"})

        user = User.query.filter_by(id=id).first()
        result = dict()
        if user is None:
            return {"Content": "User not found"}

        User.query.filter_by(id=id).delete()
        from server import db
        db.session.commit()
        result["Success"] = "User deleted"
        # print(type(result))
        return jsonify(result)