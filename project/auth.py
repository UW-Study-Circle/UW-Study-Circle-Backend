# auth.py
import re
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from server import db, app, mail
from threading import Thread
from flask_mail import Message


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()
    if not user:
        user = User.query.filter_by(email=name).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    
    # next = flask.request.args.get('next')
    # # is_safe_url should check if the url is safe for redirects.
    # # See http://flask.pocoo.org/snippets/62/ for an example.
    # if not is_safe_url(next):
    #     return flask.abort(400)

    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm')
    email_exist = User.query.filter_by(email=email).first() 
    name_exist = User.query.filter_by(name=name).first() 
    email_match = re.search(".*@wisc.edu$", email)
    # if this returns a user, then the email already exists in database

    if email_exist: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    if name_exist: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('name already exists')
        return redirect(url_for('auth.signup'))
    
    # if not email_match: # if the email is wrong, we want to redirect back to signup page so user can try again  
    #     flash('Please register with UW-Madison email')
    #     return redirect(url_for('auth.signup'))
    
    if confirm_password != password: # if password and confirmed password do't match, return to sign up page
        flash('Confirmed password does not match')
        return redirect(url_for('auth.signup'))
    
    
    # Conditions for a valid password are:
    # 1. Should have at least one number.
    # 2. Should have at least one uppercase and one lowercase character.
    # 3. Should have at least one special symbol.
    # 4. Should be between 6 to 20 characters long. 
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    # compiling regex 
    pat = re.compile(reg)   
    # searching regex                  
    mat = re.search(pat, password) 
    if not mat: 
        flash('Password are not valid')
        return redirect(url_for('auth.signup'))
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(user):
    token = user.get_reset_token()
    print(token)
    msg = Message()
    msg.subject = "UW-Study-Circle Password Reset"
    msg.sender = app.config['MAIL_USERNAME']
    msg.recipients = [user.email]
    print(user.email)
    msg.html = render_template('reset_password_email.html', user=user, token=token)
    # Thread(target=send_async_email, args=(app._get_current_object(), msg)).start()
    # mail.send(msg)
    with app.app_context():
        mail.send(msg)

@auth.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    # print("go to email")
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email is not regisited')
            return redirect(url_for('auth.reset_request'))
        
        send_email(user)
        flash('Please check your emailbox and click the link to reset')
        # print(user.email)
    # return redirect(url_for('login'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html')

@auth.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    if request.method == 'POST':
        password = request.form.get('password')
        user.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        flash('Password is reset')
    
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', title='reset password')