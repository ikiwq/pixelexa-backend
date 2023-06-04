from flask import session, jsonify
from flask_socketio import emit, send, join_room
from extension import socketio
import chat.views as chatviews


@socketio.on('connect')
def handle_connect():
    if session['user_id'] != '-1':
        join_room(session['user_id'])


@socketio.on('message')
def message(data):
    if session['user_id'] == '-1':
        return jsonify('Not logged in'), 400

    messageText = data['message']
    recipientId = data['recipient']

    new_message = chatviews.save_message(messageText, recipientId)

    emit('message', new_message, room=session['user_id'])
    emit('message', new_message, room=recipientId)




