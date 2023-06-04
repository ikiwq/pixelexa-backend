from flask import Blueprint

import article.comment.views as comment_views

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/create/<article_id>', methods=['POST'])
def create_comment(article_id):
    return comment_views.comment_article(article_id)


@comment_bp.route('/upvote/<comment_id>', methods=['GET'])
def upvote_comment(comment_id):
    return comment_views.upvote_comment(comment_id)


@comment_bp.route('/downvote/<comment_id>', methods=['GET'])
def downvote_comment(comment_id):
    return comment_views.downvote_comment(comment_id)


@comment_bp.route('/delete/<comment_id>', methods=['GET'])
def delete_comment(comment_id):
    return comment_views.delete_comment(comment_id)


@comment_bp.route('/get/<article_id>', methods=['GET'])
def get_comments_from_article(article_id):
    return comment_views.get_comments_from_article(article_id)
