from flask_socketio import SocketIO
from flask_socketio import emit, join_room, leave_room

from flask import Blueprint, session, redirect, url_for, render_template, request

from flask_login import login_user, logout_user, login_required, current_user
from server import socketio, db
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
            session['user_id'] = current_user.id
            session['group_id'] = groupid
        else:
            return {'Error': 'Unauthenticated'}
    else:
        return {"Error": "Group not found"}
    result = Message.query.all()
    # result = Message.query.filter_by(group_id=groupid).order_by(desc(Message.id)).limit(20)
    messages = {}
    for i in result:
        messages[i.id] = (i.message,i.user_name)
        # messages.append(i.message)
        # users.append(i.user_name)
    return render_template('chat.html', name=name, room=room, messages=messages)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' joined the group'}, room=room)
    groupid = request.args.get('groupid')
    # print(groupid)
    # msghistory = Message.query.filter_by(group_id=groupid).order_by(desc(Message.id)).limit(20)
    # msghistory = Message.query.filter_by(group_id=groupid)
    # message = Message(message=message)
    # # Takes message and adds to db
    # db.session.add(message)
    # # Save changes
    # db.session.commit()


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    name = session.get('name')
    group_id=session.get('group_id')
    user_id=session.get('user_id')
    print(type(message))
    newmessage = Message(message=message['msg'],user_name=name,group_id=group_id)
    # Takes message and adds to db
    db.session.add(newmessage)
    # Save changes
    db.session.commit()
    emit('message', {'msg': session.get('name') + ': ' + message['msg'] + "\n"}, room=room)

