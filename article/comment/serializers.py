from flask import session
from article.comment.models import ArticleCommentUpVote, ArticleCommentDownVote
from marshmallow import Schema, fields, pre_dump
from auth.serializers import UserSchema

class ArticleCommentSchema(Schema):
    id = fields.Int()

    votes_count = fields.Int()
    upvoted = fields.Bool()
    downvoted = fields.Bool()

    article_id = fields.Int()
    user_id = fields.Int()

    text = fields.Str()
    created_at = fields.DateTime()

    user = fields.Nested(UserSchema())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pre_dump()
    def do_things(self, data, **kwargs):
        upvotes = ArticleCommentUpVote.query.filter_by(article_comment_id=data.article_id).count()
        downvotes = ArticleCommentDownVote.query.filter_by(article_comment_id=data.article_id).count()
        data.votes_count = upvotes - downvotes

        if session['user_id'] != -1:
            if ArticleCommentUpVote.query.filter_by(article_comment_id=data.article_id, user_id=data.user_id).first():
                data.upvoted = True
            elif ArticleCommentDownVote.query.filter_by(article_comment_id=data.article_id, user_id=data.user_id).first():
                data.downvoted = True

        return data