from flask import Blueprint, request, jsonify
import image.views as imageviews

image_bp = Blueprint('image', __name__)

@image_bp.route('/<path:path>')
def get_image(path: str):
    return imageviews.get_image(path)