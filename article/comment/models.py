from extension import db
from datetime import datetime


class ArticleCommentUpVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    article_comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id'), nullable=False)
    article_comment = db.relationship('ArticleComment', backref='upvotes', foreign_keys=[article_comment_id])

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='upvotes', foreign_keys=[user_id])


class ArticleCommentDownVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    article_comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id'), nullable=False)
    article = db.relationship('ArticleComment', backref='downwotes', foreign_keys=[article_comment_id])

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='downvotes', foreign_keys=[user_id])


class ArticleComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref='comments', foreign_keys=[article_id])

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='comments', foreign_keys=[user_id])