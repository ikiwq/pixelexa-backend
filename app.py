from flask import Flask, request, session, abort, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from extension import db

from os.path import join, dirname, realpath
from datetime import datetime
import jwt

from auth.models import User, RefreshToken

from auth.urls import auth_bp
from article.urls import article_bp
from user_interaction.urls import user_interaction_bp
from article.comment.urls import comment_bp
from category.urls import category_bp

from auth import utils


app = Flask(__name__)

#Secret key to generate JWTs
app.config['SECRET_KEY'] = 'wojdjwqoi3hj89Hh#73H4T3UHFU'
#Database url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:n7B37b**#un83@localhost/pixelexa'
#Upload folder for images
app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static', 'uploads')

#Enable CORS
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, supports_credentials=True)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix="/auth", support_credentials=True)
app.register_blueprint(article_bp, url_prefix="/article", support_credentials=True)
app.register_blueprint(user_interaction_bp, url_prefix="/interaction", support_credentials=True)
app.register_blueprint(category_bp, url_prefix="/category", support_credentials=True)
app.register_blueprint(comment_bp, url_prefix="/comment", support_credentials=True)

#This middleware will check for any auth_tokens cookies.
@app.before_request
def auth_middleware():
    auth_cookie = request.cookies.get('auth_token')
    refresh_token = request.cookies.get('refresh_token')
    if auth_cookie:
        #If there is an auth cookie, then get the user id from it.
        try:
            session['user_id'] = jwt.decode(auth_cookie, app.config['SECRET_KEY'], algorithms=['HS256']).get('id')
        #If the jwt is expired, a new one is needed.
        except jwt.ExpiredSignatureError:
            #First, get the refresh token.
            token = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256']).get('token')
            #Get the object from the databse corrisponding to the refresh token we got.
            refresh_token_object = RefreshToken.query.filter_by(token=token).first()
            #And take the user.
            user = User.query.filter_by(id=refresh_token_object.user_id).first()
            #To prevent non-existing user, retrieve it from the database.
            #Next, set the session user_id as the user's id
            session['user_id'] = user.id

            #Generate new tokens
            new_access_token = utils.generate_access_token(user)
            new_refresh_token = utils.generate_refresh_token(user)

            response = make_response()

            max_age = 60 * 60 * 24 * 365
            expires = int(datetime.utcnow().timestamp() + max_age)

            #Add the tokens to the response.
            response.set_cookie('auth_token', new_access_token, httponly=True, path='/',
                                max_age=max_age, expires=expires)
            response.set_cookie('refresh_token', new_refresh_token, httponly=True, path='/',
                                max_age=max_age, expires=expires)

            db.session.delete(refresh_token_object)
            db.session.commit()

            return response

        #If the tokens are invalid, abort.
        except jwt.InvalidTokenError:
            abort(400, description="Invalid JWT.")
    else:
        session['user_id'] = -1


if __name__ == '__main__':
    app.run(port=5000)
