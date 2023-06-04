from extension import db
from datetime import datetime


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender = db.relationship('User', backref='messages_sent', foreign_keys=[sender_id])

    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient = db.relationship('User', backref='messages_recieved', foreign_keys=[recipient_id])

    text = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)


    messages = db.relationship('ChatMessage', backref="chat")




