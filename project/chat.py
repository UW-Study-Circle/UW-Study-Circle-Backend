from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room

from flask import Blueprint, render_template

from flask_login import login_user, logout_user, login_required, current_user
from server import socketio

chat = Blueprint('chat', __name__)

@chat.route('/chat', methods=["GET", "POST"])
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@chat.route('/', methods=["GET", "POST"])
def sessions():
    return render_template('chat.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
