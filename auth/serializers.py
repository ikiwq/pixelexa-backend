from marshmallow import Schema, fields, pre_dump
from auth.models import User
from article.models import Article
from user_interaction.models import Star


class UserSchema(Schema):
    id = fields.Int()

    email = fields.Str()
    username = fields.Str()
    name = fields.Str()
    biography = fields.Str()

    total_stars = fields.Int()

    permission_level = fields.Int()

    profile_image = fields.Str()
    background_image = fields.Str()

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path', 'http://localhost:5000/image/')
        super().__init__(*args, **kwargs)

    @pre_dump()
    def do_things(self, data, **kwargs):
        if not data.profile_image.startswith("http"):
            data.profile_image = self.path + data.profile_image
        if data.background_image and not data.background_image.startswith("http"):
            data.background_image = self.path + data.background_image

        data.total_stars = Star.query.join(Article).join(User).filter(Article.creator_id == data.id).count()

        return data
