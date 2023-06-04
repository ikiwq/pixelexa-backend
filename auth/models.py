from extension import db
from chat.models import Chat
from werkzeug.security import generate_password_hash, check_password_hash

chat_user = db.Table('chat_user',
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    telephone_number = db.Column(db.Integer, unique=True, nullable=True)

    username = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    biography = db.Column(db.String(300), nullable=True, default='')

    profile_image = db.Column(db.String(100), default="default-user-image", nullable=False)
    background_image = db.Column(db.String(100), nullable=True)

    birth = db.Column(db.DateTime, nullable=True)

    permission_level = db.Column(db.Integer, default="0", nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    is_muted = db.Column(db.Boolean, default=False)

    chats = db.relationship(Chat, secondary=chat_user, backref='users')

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(128), nullable=False)
