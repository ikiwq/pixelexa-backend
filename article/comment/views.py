from flask import session, request, jsonify
from article.comment.models import ArticleComment, ArticleCommentUpVote, ArticleCommentDownVote
from article.comment.serializers import ArticleCommentSchema
from article.models import Article
from sqlalchemy import desc, asc
from extension import db


def upvote_comment(comment_id):
    upvote = ArticleCommentUpVote.query.filter_by(article_comment_id=comment_id, user_id=session['user_id']).first()
    if upvote:
        db.session.delete(upvote)
        db.session.commit()
        return jsonify({"message": "Removed upvote from comment"})

    upvote = ArticleCommentUpVote(
        article_comment_id=comment_id,
        user_id=session['user_id']
    )

    db.session.add(upvote)
    db.session.commit()

    return jsonify({"message": "Comment upvoted"})


def downvote_comment(comment_id):
    downvote = ArticleCommentDownVote.query.filter_by(article_comment_id=comment_id, user_id=session['user_id']).first()
    if downvote:
        db.session.delete(downvote)
        db.session.commit()
        return jsonify({"message": "Removed downvote from comment"})

    downvote = ArticleCommentDownVote(
        article_comment_id=comment_id,
        user_id=session['user_id']
    )

    db.session.add(downvote)
    db.session.commit()

    return jsonify({"message": "Comment downvoted"})


def delete_comment(comment_id):
    comment = ArticleComment.query.filter_by(id=comment_id).first()
    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    if comment.user.id != session['user_id']:
        return jsonify({"message": "Not allowed"}), 401

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted"})


def comment_article(article_id):
    data = request.json

    article = Article.query.filter_by(id=article_id).first()
    if not article:
        return jsonify({"message": "Article not found"}), 404

    new_comment = ArticleComment(
        text=data.get('text'),
        user_id=session['user_id'],
        article_id=article.id
    )

    db.session.add(new_comment)
    db.session.commit()

    comment_schema = ArticleCommentSchema()
    comment_data = comment_schema.dump(new_comment)

    return jsonify(comment_data)


def get_comments_from_article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if not article:
        return jsonify({"message": "Article not found."}), 404

    cursor = request.args.get("cursor", default=-1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)

    if cursor != -1:
        comments = ArticleComment.query.order_by(desc(ArticleComment.id))\
            .filter_by(article_id=article_id).filter(ArticleComment.id < cursor).limit(page_size)
    else:
        comments = ArticleComment.query.order_by(desc(ArticleComment.id))\
            .filter_by(article_id=article_id).limit(page_size)

    comments_schema = ArticleCommentSchema()

    comments_data = comments_schema.dump(comments, many=True)


    return jsonify(comments_data)

