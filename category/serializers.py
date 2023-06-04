from marshmallow import Schema, fields, pre_dump
from article.models import Article
from category.models import Category
from datetime import datetime, timedelta

class CategorySchema(Schema):
    id = fields.Int()

    name = fields.Str()
    created_at = fields.DateTime()

    articles_last_day = fields.Int()
    articles_last_7_days = fields.Int()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pre_dump()
    def do_things(self, data, **kwargs):
        last_day = datetime.now() - timedelta(days=1)
        data.articles_last_day = Article.query.join(Category, Article.categories)\
            .filter(Article.created_at >= last_day, Category.name == data.name).count()

        last_week = datetime.now() - timedelta(days=7)
        data.articles_last_7_days = Article.query.join(Category, Article.categories) \
            .filter(Article.created_at >= last_week, Category.name == data.name).count()

        return data