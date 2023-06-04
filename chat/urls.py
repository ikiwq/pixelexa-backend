from flask import Blueprint
import chat.views as chatviews

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/', methods=['GET'])
def get_all_chats_from_user():
    return chatviews.get_all_chats_from_user()


@chat_bp.route('/<username>', methods=['GET'])
def get_chat_with_user(username):
    return chatviews.get_chat_with_user(username)