from extension import db
from datetime import datetime

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref='posts')

    title = db.Column(db.String(100))
    excerpt = db.Column(db.String(350))
    content = db.Column(db.String(7500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    stars_count = db.Column(db.Integer, default=0)
    saves_count = db.Column(db.Integer, default=0)
    impressions = db.Column(db.Integer, default=0)

    image = db.Column(db.String(100), nullable=True)
