from flask import jsonify, session
from user_interaction.models import Star, Save
from extension import db


def star_article(article_id):
    star = Star.query.filter_by(user_id=session['user_id'], article_id=article_id).first()

    if star:
        db.session.delete(star)
        db.session.commit()

        message = jsonify({"message": "Star removed from post"})
        return message, 200

    star = Star(
        article_id=article_id,
        user_id=session['user_id']
    )

    db.session.add(star)
    db.session.commit()

    message = jsonify({"message": "Post starred"})
    return message, 200


def save_article(article_id):
    save = Save.query.filter_by(user_id=session['user_id'], article_id=article_id).first()
    if save:
        db.session.delete(save)
        db.session.commit()

        return jsonify({"message": "Save removed"}), 200

    save = Save(
        article_id=article_id,
        user_id=session['user_id']
    )

    db.session.add(save)
    db.session.commit()

    return jsonify({"message": "Article saved"}), 200
