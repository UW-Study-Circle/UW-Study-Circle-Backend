from flask import Response, request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_apispec import doc, use_kwargs
from flask_apispec.views import MethodResource

from models import User, UserSchema, Group, GroupSchema
user_schema = UserSchema()
group_schema = GroupSchema()

class HelloAPI(MethodResource, Resource):
    @doc(description='Hello World API.', tags=['Hello-World'])
    def get(self):
        '''
        Get method represents a Hello World GET API method
        '''
        return {'hello': 'world'}

class UserAPI(MethodResource, Resource):
    @doc(description='Post request for signup feature.', tags=['User'])
    @use_kwargs(UserSchema)
    def post(self):
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
            phone = body["phone"]         
            
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
    def get(self, email):
        '''
        Get method for User Login
        '''
        user = User.query.filter_by(email=email).first()
        result = dict()
        if user is None:
            return {"Content": None}

        result["Content"] = user_schema.dump(user)
        # print(type(result))
        return jsonify(result)

    @doc(description='Delete request for delete account feature.', tags=['User'])
    def delete(self, id):
        '''
        Delete method for User deletion
        '''
        user = User.query.filter_by(id=id).first()
        result = dict()
        if user is None:
            return {"Content": "User not found"}

        User.query.filter_by(id=id).delete()
        result["Success"] = "User deleted"
        # print(type(result))
        return jsonify(result)

class GroupAPI(Resource):
    @doc(description='Post request for group creation feature.', tags=['Group'])
    @use_kwargs(GroupSchema)
    def post(self):
        body = request.get_json()
        if body is None:
            return jsonify({"Error": "Data not in correct format"})
        print(body)
        
        result = dict()
        try:
            groupname = body["groupname"]
            groupid = body["groupid"]
            courseinfo = body["courseinfo"]
            level = body["level"]
            description = body["description"]
            capacity = body["capacity"]
            duration = body["duration"]
            status = body["status"]         
                
            groupname_exist = Group.query.filter_by(groupname=groupname).first() 
            if groupname_exist:
                result["Duplicate"] = "Group Name already exists"
                return jsonify(result)   
            new_group = Group(
                groupname=groupname, groupid=groupid, courseinfo=courseinfo, level=level, description=description,
                capacity=capacity, duration=duration, status=status)
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
    @doc(description='Get request for search feature by groupname.', tags=['Group'])
    def get(self, groupname):
        group = Group.query.filter_by(groupname=groupname).first()
        result = dict()
        if group is None:
            return {"Content": None}

        result["Content"] = group_schema.dump(group)
        # print(type(result))
        return jsonify(result)
    @doc(description='Delete request for delete group feature.', tags=['Group'])
    def delete(self, id):
        group = Group.query.filter_by(groupid=groupid).first()
        result = dict()
        if group is None:
            return {"Content": "Group not found"}

        Group.query.filter_by(groupid=groupid).delete()
        result["Success"] = "Group deleted"
        # print(type(result))
        return jsonify(result)