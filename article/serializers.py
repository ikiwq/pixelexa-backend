from flask import session

from marshmallow import Schema, fields, pre_dump

from user_interaction.models import Star, Save
from article.comment.models import ArticleComment

from auth.serializers import UserSchema
from category.serializers import CategorySchema


class ArticleSchema(Schema):
    id = fields.Int()

    creator = fields.Nested(UserSchema())
    categories = fields.Nested(CategorySchema(), many=True)

    title = fields.Str()
    content = fields.Str()
    excerpt = fields.Str()

    created_at = fields.DateTime()

    image = fields.Str()

    stars_count = fields.Integer()
    saves_count = fields.Integer()
    comments_count = fields.Integer()
    impressions = fields.Integer()

    starred = fields.Boolean()
    saved = fields.Boolean()

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path', 'http://localhost:5000/image/')
        super().__init__(*args, **kwargs)

    @pre_dump()
    def do_things(self, data, **kwargs):
        #before the dump, check if the image has been "urlified"
        #otherwise urlify it.
        if not data.image.__contains__('http://localhost:5000/image/'):
            data.image = self.path + data.image

        data.stars_count = Star.query.filter_by(article_id=data.id).count()
        data.saves_count = Save.query.filter_by(article_id=data.id).count()
        data.comments_count = ArticleComment.query.filter_by(article_id=data.id).count()
        #If the user is logged in, try to check if the article is starred or saved
        try:
            if session['user_id'] != -1:
                if Star.query.filter_by(article_id=data.id, user_id=session['user_id']).first():
                    data.starred = True
                if Save.query.filter_by(article_id=data.id, user_id=session['user_id']).first():
                    data.saved = True
        except Exception as e:
            print(e)

        return data
