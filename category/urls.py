from flask import Blueprint
import category.view as category_views

category_bp = Blueprint('category', __name__)


@category_bp.route('/most_popular', methods=['GET'])
def most_popular_categories():
    return category_views.get_most_popular_categories()


@category_bp.route('/by_name/<name>', methods=['GET'])
def get_by_name(name):
    return category_views.get_by_name(name)
