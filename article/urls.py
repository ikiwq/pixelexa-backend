from flask import Blueprint, request
import article.views as article_views

article_bp = Blueprint('article', __name__)


@article_bp.route('', methods=['GET'])
def get_articles():
    return article_views.get_articles()


@article_bp.route('/create/', methods=['POST'])
def create_article():
    return article_views.create()


@article_bp.route('/id/<article_id>', methods=['GET', 'DELETE'])
def get_single_article(article_id):
    if request.method == "GET":
        return article_views.get_single_article(article_id)
    if request.method == "DELETE":
        return article_views.delete_article(article_id)


@article_bp.route('/similar', methods=['GET'])
def similar_articles():
    return article_views.get_similar_articles()
