import jwt
from .models import User, RefreshToken
from flask import current_app
from datetime import datetime, timedelta
from uuid import uuid4
import re
from extension import db


def generate_access_token(user: User):
    payload = {"id": user.id, "exp": datetime.now() + timedelta(minutes=15)}
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def generate_refresh_token(user: User):
    token = str(uuid4())
    refreshToken = RefreshToken(
        user_id=user.id,
        token=token
    )

    payload = {"token": token}

    db.session.add(refreshToken)
    db.session.commit()

    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def validate_email(email):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    return False


def validate_password(password):
    pass


def is_name_valid(username):
    pass
