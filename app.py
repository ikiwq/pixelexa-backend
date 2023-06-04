from flask import Flask, request, session, abort, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from extension import db, socketio

from os.path import join, dirname, realpath
from datetime import datetime
import jwt

from auth.models import User, RefreshToken

from chat.urls import chat_bp
from auth.urls import auth_bp
from image.urls import image_bp
from article.urls import article_bp
from user_interaction.urls import user_interaction_bp
from article.comment.urls import comment_bp
from category.urls import category_bp

from auth import utils


app = Flask(__name__)

app.config['SECRET_KEY'] = 'wojdjwqoi3hj89Hh#73H4T3UHFU'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:n7B37b**#un83@localhost/pixelexa'
app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static', 'uploads')

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, supports_credentials=True)

db.init_app(app)
migrate = Migrate(app, db)
socketio.init_app(app, cors_allowed_origins='*')

with app.app_context():
    db.create_all()

import server_socket.buckets

app.register_blueprint(auth_bp, url_prefix="/auth", support_credentials=True)
app.register_blueprint(image_bp, url_prefix="/image", support_credentials=True)
app.register_blueprint(article_bp, url_prefix="/article", support_credentials=True)
app.register_blueprint(chat_bp, url_prefix="/chat", support_credentials=True)
app.register_blueprint(user_interaction_bp, url_prefix="/interaction", support_credentials=True)
app.register_blueprint(category_bp, url_prefix="/category", support_credentials=True)
app.register_blueprint(comment_bp, url_prefix="/comment", support_credentials=True)

@app.before_request
def auth_middleware():
    auth_cookie = request.cookies.get('auth_token')
    refresh_token = request.cookies.get('refresh_token')
    if auth_cookie:
        try:
            session['user_id'] = jwt.decode(auth_cookie, app.config['SECRET_KEY'], algorithms=['HS256']).get('id')
        except jwt.ExpiredSignatureError:
            token = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256']).get('token')

            refresh_token_object = RefreshToken.query.filter_by(token=token).first()
            user = User.query.filter_by(id=refresh_token_object.user_id).first()

            session['user_id'] = user.id

            new_access_token = utils.generate_access_token(user)
            new_refresh_token = utils.generate_refresh_token(user)

            response = make_response()

            max_age = 60 * 60 * 24 * 365
            expires = int(datetime.utcnow().timestamp() + max_age)

            response.set_cookie('auth_token', new_access_token, httponly=True, path='/',
                                max_age=max_age, expires=expires)
            response.set_cookie('refresh_token', new_refresh_token, httponly=True, path='/',
                                max_age=max_age, expires=expires)

            db.session.delete(refresh_token_object)
            db.session.commit()

            return response

        except jwt.InvalidTokenError:
            abort(400, description="Invalid JWT.")
    else:
        session['user_id'] = -1


if __name__ == '__main__':
    socketio.run(app, debug=True)
