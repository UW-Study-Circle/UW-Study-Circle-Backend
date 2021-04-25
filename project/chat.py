from flask_socketio import SocketIO
from flask_socketio import emit, join_room, leave_room

from flask import Blueprint, session, redirect, url_for, render_template, request

from flask_login import login_user, logout_user, login_required, current_user
from server import socketio
from models import Group, GroupSchema, Message, Member

from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

from sqlalchemy import desc

chat = Blueprint('chat', __name__)

class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    submit = SubmitField('Enter Chatroom')


# @chat.route('/chat', methods=["GET", "POST"])
# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')

@chat.route('/chat', methods=["GET", "POST"])
def sessions():
    """Chat room. The user's name and room must be stored in
    the session."""
    groupid = request.args.get('groupid')
    group = Group.query.get(groupid)
    name = ""
    room = ""
    # Get the user id from current user, check member model exists and pending false, part of group
    if group:
        if current_user.is_authenticated:
            name = current_user.username
            room = group.groupname
            session['room'] = group.groupname
            session['name'] = name
        else:
            return {'Error': 'Unauthenticated'}
    else:
        return {"Error": "Group not found"}
    return render_template('chat.html', name=name, room=room)


# @chat.route('/chatlogin', methods=["GET", "POST"])
# def index():
#     """Login form to enter a room."""
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['name'] = form.name.data
#         session['room'] = form.room.data
#         return render_template('chat.html', room=session['room'])
#     elif request.method == 'GET':
#         form.name.data = session.get('name', '')
#         form.room.data = session.get('room', '')
#     return render_template('index.html', form=form)

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' joined the group'}, room=room)
    groupid = request.args.get('groupid')
    msghistory = Message.query.filter_by(group_id=groupid).order_by(desc(Message.id)).limit(20)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ': ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


# @chat.route('/demo', methods=["GET", "POST"])
# def sessions():
#     return render_template('index.html')

# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print(current_user)
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)
