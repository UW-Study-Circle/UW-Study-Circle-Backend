<<<<<<< HEAD
# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from server import db, app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/creategroup')
@login_required
def creategroup():
    if request.method == 'POST':
        groupname = request.form.get('Group Name')
        description = request.form.get('Group Description')
        courseInfo = request.form.get('UW-Madison Course Name & Number')
        capacity = request.form.get('Group Capacity')
        duration = request.form.get('Period of Study')
        status = request.form.get('Status')
    if groupname or description or courseInfo or capacity or duration or status is None:
        flash('Please fill in all the required fields.')
        return redirect(url_for('main.creategroup'))
    groupname_exist = Group.query.filter_by(groupname=groupname).first() 
    if groupname:
        flash('Group name already exists. Please enter a new group name.')
        return redirect(url_for('main.creategroup'))
        # add the new user to the database
    if capacity > 50:
        flash('The maximum allowed capacity is 50 students.')
    new_group = Group(groupname=groupname, description=description, courseInfo=courseInfo, capacity=capacity,
    duration=duration, status=status)
    db.session.add(new_group)
    db.session.commit()
    return render_template('creategroup.html')

@main.route('/viewallgroups')
@login_required
def viewallgroups():
    allGroups = Group.query.all();
=======
# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from server import db, app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/creategroup')
@login_required
def creategroup():
    groupname = request.form.get('Group Name')
    description = request.form.get('Group Description')
    courseInfo = request.form.get('UW-Madison Course Name & Number')
    capacity = request.form.get('Group Capacity')
    duration = request.form.get('Period of Study')
    status = request.form.get('Status')
    groupname_exist = Group.query.filter_by(groupname=groupname).first() 
    if groupname:
        flash('Group name already exists. Please enter a new group name.')
        # add the new user to the database
    new_group = Group(groupname=groupname, email=email, description=description, courseInfo=courseInfo, capacity=capacity,
    duration=duration, status=status)
    db.session.add(new_group)
    db.session.commit()
    return render_template('creategroup.html')

@main.route('/viewallgroups')
@login_required
def viewallgroups():
    allGroups = Group.query.all();
>>>>>>> e3e965d (Updated models.py)
