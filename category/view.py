from flask import request, jsonify
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from article.models import Article
from category.models import Category
from category.serializers import CategorySchema

def get_most_popular_categories():
    page_size = request.args.get('page_size', default=5, type=int)

    start_date = datetime.now() - timedelta(days=7)

    categories = Category.query.join(Article, Category.articles)\
        .group_by(Category.id).order_by(desc(func.count(Article.id))).limit(page_size).all()

    categories_schema = CategorySchema()
    categories_data = categories_schema.dump(categories, many=True)

    return jsonify(categories_data)

def get_by_name(name):
    category = Category.query.filter_by(name=name).first()

    category_schema = CategorySchema()
    category_data = category_schema.dump(category)

    return jsonify(category_data)