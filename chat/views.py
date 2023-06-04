from flask import session
from extension import db
from .models import ChatMessage, Chat
from auth.models import User
from chat.serializers import ChatMessageSchema, ChatSchema


def get_all_chats_from_user():
    chats = Chat.query.filter(Chat.users.any(id=session['user_id']))


def save_message(text, recipient_id):
    new_message = ChatMessage()

    user1 = User.query.filter_by(id=recipient_id).first()
    user2 = User.query.filter_by(id=session['user_id']).first()

    chat = Chat.query.filter(Chat.users.any(id=user1.id), Chat.users.any(id=user2.id)).first()

    if not chat:
        chat = Chat()
        chat.users.append(user1)
        chat.users.append(user2)

        db.session.add(chat)
        db.session.commit()

    new_message.text = text
    new_message.recipient_id = recipient_id
    new_message.sender_id = session['user_id']
    new_message.chat_id = chat.id

    db.session.add(new_message)
    db.session.commit()

    message_schema = ChatMessageSchema()

    return message_schema.dump(new_message)


def get_chat_with_user(username):
    user1 = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(id=session['user_id']).first()

    chat = Chat.query.filter(Chat.users.any(id=user1.id), Chat.users.any(id=user2.id)).first()

    if not chat:
        chat = Chat()
        chat.users.append(user1)
        chat.users.append(user2)

        db.session.add(chat)
        db.session.commit()

    chat_schema = ChatSchema()

    return chat_schema.dump(chat)
