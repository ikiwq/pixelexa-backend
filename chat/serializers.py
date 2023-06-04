from marshmallow import Schema, fields
from auth.serializers import UserSchema


class ChatMessageSchema(Schema):
    id = fields.Int()

    sender = fields.Nested(UserSchema())
    recipient = fields.Nested(UserSchema())

    text = fields.Str()
    image = fields.Str()

    created_at = fields.DateTime()


class ChatSchema(Schema):
    id = fields.Int()

    users = fields.Nested(UserSchema(), many=True)
