from flask import request, jsonify, session, current_app, make_response
from .models import User, RefreshToken
from .utils import generate_access_token, generate_refresh_token, validate_email
from os.path import join
from extension import db
from uuid import uuid4
from auth.serializers import UserSchema
import json
from datetime import datetime
import jwt

max_age = 60 * 60 * 24 * 365
expires = int(datetime.utcnow().timestamp() + max_age)


def get_current_user():
    user = User.query.filter_by(id=session['user_id']).first()
    return user


def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User does not exists.'}), 400
    if not user.verify_password(password):
        return jsonify({'message': 'Invalid credentials.'}), 400

    response = jsonify({'email': user.email})

    token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie('auth_token', token, httponly=True, path='/',
                        max_age=max_age, expires=expires)
    response.set_cookie('refresh_token', refresh_token, httponly=True, path='/',
                        max_age=max_age, expires=expires)

    return response


def register():
    data = request.form.get('data')
    data = json.loads(data)

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    username = data.get('username')

    image_file = request.files.get('profile_image')

    if not validate_email(email):
        return jsonify({'message': 'Please insert a valid email.'}), 400

    if not password or password == '':
        return jsonify({'message': 'Please insert a valid password.'}), 400

    if not name or name == '':
        return jsonify({'message': 'Please insert a valid name.'}), 400

    if not username or username == '':
        return jsonify({'message': 'Please insert a valid username.'}), 400

    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'User with that email already exists'}), 409
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'User with that username already exists'}), 409

    image_name = str(uuid4())
    if image_file is not None:
        UPLOADS_PATH = join(current_app.config['UPLOAD_FOLDER'], 'images')
        image_file.save(join(UPLOADS_PATH, image_name + '.jpg'))

    user = User(
        email=data.get('email'),
        password=data.get('password'),
        name=data.get('name'),
        username=data.get('username'),
        profile_image=image_name if image_file is not None else "default-user-image"
    )

    db.session.add(user)
    db.session.commit()

    response = jsonify({'email': user.email, 'message': 'User created successfully.'})
    token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie('auth_token', token, httponly=True, path='/',
                        max_age=max_age, expires=expires)
    response.set_cookie('refresh_token', refresh_token, httponly=True, path='/',
                        max_age=max_age, expires=expires)

    return response, 201


def logout():
    refresh_token = request.cookies.get('refresh_token')
    token = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256']).get('token')
    refresh_token_object = RefreshToken.query.filter_by(token=token).first()

    if refresh_token_object:
        db.session.delete(refresh_token_object)
        db.session.commit()

    response = make_response()

    response.set_cookie('auth_token', '', httponly=True, path='/', expires=0)
    response.set_cookie('refresh_token', '', httponly=True, path='/', expires=0)

    return response

def get_users_by_username(username):
    users = User.query.filter(User.username.like(f'%{username}%')).all()

    user_schema = UserSchema()
    users_data = user_schema.dump(users, many=True)

    return jsonify(users_data)


def get_user_by_username(username):
    user = User.query.filter_by(username = username).first()

    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return jsonify(user_data)
