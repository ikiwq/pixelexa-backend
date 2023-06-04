from flask import Blueprint, jsonify
from auth.serializers import UserSchema
import auth.views as authviews

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login/', methods=['POST'])
def login():
    return authviews.login()


@auth_bp.route('/register/', methods=['POST'])
def register():
    return authviews.register()


@auth_bp.route('/logout/', methods=['GET'])
def logout():
    return authviews.logout()


@auth_bp.route('/get_current_user/', methods=['GET'])
def get_current_user():
    user_schema = UserSchema()
    user_dict = user_schema.dump(authviews.get_current_user())
    return jsonify(user_dict)


@auth_bp.route('/get_users_by_username/<username>', methods=['GET'])
def get_users_by_name(username):
    return authviews.get_users_by_username(username)


@auth_bp.route('/get_user_by_username/<username>', methods=['GET'])
def get_user_by_name(username):
    return authviews.get_user_by_username(username)
