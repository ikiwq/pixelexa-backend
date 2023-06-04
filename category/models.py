from extension import db
from datetime import datetime

category_article = db.Table(
    'category_article',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    articles = db.relationship('Article', secondary=category_article, backref=db.backref('categories'))