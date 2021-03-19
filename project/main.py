# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

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

@auth.route('/signup', methods=['GET,'POST'])
def signup_post():

    firstname = request.form.get('First Name')
    lastname = request.form.get('Last Name')
    email = request.form.get('Email')
    username = request.form.get('Username')
    password = request.form.get('Password')
    phonenumber = request.form.get('Phone Number')
    gender = request.form.get('Gender')


    print(request.form)
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    # Check the username before creating new user
    q = User.query.filter_by(username=username)
    if user: # if a username for a user is found, alert with message
        flash('This username has already been taken.')
    # Check password before creating new user
    # Conditions for checking: The password should be at least 6 characters long 
    # have 1 upper case letter, 1 lower case letter, 1 number and 1 punctuation.
    while True:
        if not any(p.islower() for p in password): 
            flash("This is NOT a valid password")
        elif not any(p.isupper() for p in password): 
            flash("This is NOT a valid password")
        elif not any(p.isdigit() for p in password):
            flash("This is NOT a valid password")
        elif len(password) < 6:
            flash("This is NOT a valid password")
        else:
            flash("This is a valid password")
            break
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, firstname=firstname, lastname = lastname, username = username
                password=generate_password_hash(password, method='sha256'),
                address = address,
                phonenumber = phonenumber
                gender = gender
                )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
