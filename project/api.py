from flask import Response, request, jsonify
from flask_restful import Resource
from webargs import fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_apispec import doc, use_kwargs, marshal_with
from flask_apispec.views import MethodResource

from models import User, UserSchema, Group, GroupSchema
user_schema = UserSchema()
group_schema = GroupSchema(many=True)

from flask_login import login_user, logout_user, login_required, current_user

class ProfileAPI(MethodResource, Resource):
    @doc(description='User Profile API.', tags=['User-Profile'])
    def get(self, id=None, logout=False):
        '''
        Get method to fetch logged-in user's profile
        '''
        if current_user.is_authenticated:
            if logout:
                logout_user()
                return {"Logout Successful!": True}
            if id == None:
                return user_schema.dump(current_user)
            else:
                result = dict()
                user = User.query.get(id)
                if user:
                    result["username"] = user.username
                    result["firstname"] = user.firstname
                    result["lastname"] = user.lastname
                else:
                    result["username"] = None
                return jsonify(result)
        return {'Error': 'Unauthenticated'}
    
    @doc(description='Login User API.', tags=['User-Profile'])
    @use_kwargs({
        'email': fields.Str(),
        'password': fields.Str()
    })
    def post(self, **kwargs):
        '''
        Post method for User Login
        '''
        body = request.get_json()
        if body is None:
            return jsonify({"Error": "Data not in correct format"})
        print(body)
        result = dict()
        try:
            email = body["email"]
            password = body["password"]
            user = User.query.filter_by(email=email).first()
            print(user)
            if not user or not check_password_hash(user.password, password): 
                return {"Content": None} # if user doesn't exist or password is wrong, reload the page

            # if the above check passes, then we know the user has the right credentials
            login_user(user, remember=True)
            
            
            result["Content"] = user_schema.dump(user)
        except Exception as e:
            result["Error"] = str(e)
        # print(type(result))
        return jsonify(result)


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

class GroupAPI(MethodResource, Resource):
    @doc(description='Post request for group creation feature.', tags=['Group'])
    @use_kwargs(GroupSchema)
    @login_required
    def post(self, **kwargs):
        body = request.get_json()
        if body is None:
            return jsonify({"Error": "Data not in correct format"})
        print(body)
        
        result = dict()
        try:
            groupname = body["groupname"]
            courseinfo = body["courseinfo"]
            level = body["level"]
            description = body["description"]
            capacity = body["capacity"]
            duration = body["duration"]
            status = body["status"]         
            admin_id = current_user.id

            groupname_exist = Group.query.filter_by(groupname=groupname).first() 
            if groupname_exist:
                result["Duplicate"] = "Group Name already exists"
                return jsonify(result)   
            new_group = Group(
                groupname=groupname, courseinfo=courseinfo, level=level, description=description,
                capacity=capacity, duration=duration, status=status, admin=admin_id)
            # add the new group to the database
            from server import db

            db.session.add(new_group)
            db.session.commit()
            result["Success"] = "Group created"
            return jsonify(result)
            
        except Exception as e:
            error = dict()
            error["Error"] = str(e)
            return jsonify(error)

    @doc(description='Get all Groups.', tags=['Group'])
    @login_required
    def get(self):
        groups = Group.query.all()
        result = dict()
        print(groups)
        if groups is None:
            return {"Content": None}

        result["Content"] = group_schema.dump(groups)
        # print(type(result))
        return jsonify(result)

    @doc(description='Delete request for delete group feature.', tags=['Group'])
    @login_required
    def delete(self, id):
        group = Group.query.filter_by(groupid=groupid).first()
        result = dict()
        if group is None:
            return {"Content": "Group not found"}

        c_user_id = current_user.id
        if c_user_id == group.admin:
            Group.query.filter_by(groupid=groupid).delete()
            result["Success"] = "Group deleted"
        else:
            result["Error"] = "Not admin"
        # print(type(result))
        return jsonify(result)