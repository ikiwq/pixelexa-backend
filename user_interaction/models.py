from extension import db
from datetime import datetime


class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref='stars')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='stars')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Save(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref='saves')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='saves')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
