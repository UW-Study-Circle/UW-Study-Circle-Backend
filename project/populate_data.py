import json
from server import db, app
from models import User, Group
from werkzeug.security import generate_password_hash, check_password_hash

app.app_context().push()

with open('data.json') as f:
    data = json.load(f)

users = data["users"]
groups = data["groups"]




for user in users:
    username = user["username"]
    password = user["password"]
    email = user["email"]
    firstname = user["firstname"]
    lastname = user["lastname"]
    gender = user["gender"]
    bday = user["bday"]
    phone = user["phonenumber"]    
    new_user = User(
        email=email, username=username, password=generate_password_hash(password, method='sha256'),
        lastname=lastname, firstname=firstname, gender=gender, bday=bday, phonenumber=phone
        )
        
    db.session.add(new_user)

for group in groups:
    groupname = group["groupname"]
    courseinfo = group["courseinfo"]
    level = group["level"]
    description = group["description"]
    capacity = group["capacity"]
    duration = group["duration"]
    status = group["status"]         
    admin_id = group["admin"]      
    new_group = Group(
        groupname=groupname, courseinfo=courseinfo, level=level, description=description,
        capacity=capacity, duration=duration, status=status, admin=admin_id
        )
    db.session.add(new_group)

db.session.commit()
User.query.all()
Group.query.all()