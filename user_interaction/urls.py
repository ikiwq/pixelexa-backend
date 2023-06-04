from flask import Blueprint, jsonify
import user_interaction.views as interaction_views

user_interaction_bp = Blueprint('user_interaction', __name__)


@user_interaction_bp.route('/star_article/<article_id>', methods=['GET'])
def star_article(article_id):
    return interaction_views.star_article(article_id)
