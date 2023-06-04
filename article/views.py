from flask import request, current_app, session, jsonify

from sqlalchemy import desc, func, text
from sqlalchemy.orm import contains_eager
from extension import db

import json
from uuid import uuid4
from os.path import join

from auth.models import User
from article.models import Article
from user_interaction.models import Star
from category.models import Category

from article.serializers import ArticleSchema


def create():
    image_file = request.files.get('image')

    UPLOADS_PATH = join(current_app.config['UPLOAD_FOLDER'], 'images')

    image_name = str(uuid4())
    print(image_name)
    image_file.save(join(UPLOADS_PATH, image_name + '.jpg'))

    data = request.form.get('data')
    data = json.loads(data)

    user = User.query.filter_by(id=session['user_id']).first()

    article = Article(
        creator_id=user.id,
        title=data['title'],
        content=data['content'],
        excerpt=data['excerpt']
    )

    article.image = image_name

    if data['categories']:
        for category in data['categories']:
            category_obj = Category.query.filter_by(name=category).first()

            if not category_obj:
                category_obj = Category(
                    name=category,
                )

            category_obj.articles.append(article)

            db.session.add(category_obj)
            db.session.commit()

    db.session.add(article)
    db.session.commit()

    article_schema = ArticleSchema()
    article_data = article_schema.dump(article, many=False)

    return jsonify(article_data)


def delete_article(article_id):
    pass


def get_single_article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if not article:
        return jsonify({"message": "Article not found."}), 404

    article_schema = ArticleSchema()
    article_data = article_schema.dump(article)
    return jsonify(article_data)


def get_similar_articles():
    article_title = request.args.get("title")
    cursor = request.args.get("cursor", default=-1, type=int)
    page_size = request.args.get("page_size", default=5, type=int)

    if cursor == -1:
        query = text("SELECT article.id FROM article WHERE MATCH(title) AGAINST(:article_title IN NATURAL LANGUAGE "
                     "MODE) AND (title) <> :article_title LIMIT :page_size")
        articles = db.session.execute(query, {'article_title': article_title, 'page_size': page_size}).fetchall()
    else:
        query = text("SELECT article.id FROM article WHERE MATCH(title) AGAINST(:article_title IN NATURAL LANGUAGE "
                     "MODE) AND (title) <> :article_title AND article.id < :cursor LIMIT :page_size")
        articles = db.session.execute(query, {'article_title': article_title, 'page_size': page_size, 'cursor': cursor}).fetchall()

    articles_obj = []

    for article in articles:
        obj = Article.query.filter_by(id=article.id).first()
        if obj:
            articles_obj.append(obj)

    if articles_obj:
        article_schema = ArticleSchema()
        article_data = article_schema.dump(articles_obj, many=True)
        return jsonify(article_data)
    else:
        return jsonify([])


def get_articles():
    order = request.args.get('order', default="RECENT")
    cursor = request.args.get('cursor', type=int, default=-1)
    page_size = request.args.get('page_size', type=int, default=20)

    category = request.args.get('category', type=str, default="NONE")
    user = request.args.get('user', type=str, default="NONE")

    query = Article.query

    if category != "NONE":
        query = query.join(Article.categories)\
            .options(contains_eager(Article.categories)).filter(Category.name.like(category))

    if user != "NONE":
        user_model = User.query.filter_by(username=user).first()
        query = query.join(Article.creator)\
            .filter(Article.creator == user_model)

    if order == "CREATED_AT":
        query = query.order_by(desc(Article.id))
    if order == "POPULARITY":
        query = query.outerjoin(Star) \
            .group_by(Article.id).order_by(func.count(Star.id).desc())

    if cursor != -1:
        query = query.filter(Article.id < cursor)
    query = query.limit(page_size)

    articles = query.all()

    article_schema = ArticleSchema()
    article_data = article_schema.dump(articles, many=True)

    return jsonify(article_data)






