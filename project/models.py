# models.py

from flask_login import UserMixin
from server import db, app
import jwt
from time import time
from marshmallow import Schema, fields


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    gender = db.Column(db.String(1000))
    bday = db.Column(db.String(1000))
    phonenumber = db.Column(db.String(100), nullable=True)

class Group(UserMixin, db.Model):
    groupname = db.Column(db.String(1000), unique=True)
    id = db.Column(db.Integer, primary_key=True)
    courseinfo = db.Column(db.String(1000))
    level = db.Column(db.String(1000))
    description = db.Column(db.String(2000), nullable=True)
    capacity = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    status = db.Column(db.String(100))
    admin = db.Column(db.Integer) #userID of admin

class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    pending = db.Column(db.Boolean)

class MemberSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    group_id = fields.Int()
    pending = fields.Bool()

class MemberApprovalSchema(Schema):
    request_id = fields.Int()
    group_id = fields.Int()
    approval = fields.Bool()

class ResetPasswordSchema(Schema):
    cpwd = fields.Str()
    npwd = fields.Str()
    cnpwd = fields.Str()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    firstname = fields.Str()
    lastname = fields.Str()
    gender = fields.Str()
    bday = fields.Str()
    formatted_name = fields.Method("format_name", dump_only=True)
    phonenumber = fields.Str()
    def format_name(self, user):
        return "{}".format(user.username)

    
   

class GroupSchema(Schema):
    groupname = fields.Str()
    id = fields.Int(dump_only=True)
    courseinfo = fields.Str()
    level = fields.Str()
    description = fields.Str()
    capacity = fields.Int()
    duration = fields.Int()
    status = fields.Str()
    admin = fields.Int() # userID
    def format_name(self, group):
        return "{}".format(group.groupname)
