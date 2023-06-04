from os.path import join, dirname, realpath
import os
import uuid
from flask import request, send_file, current_app
from werkzeug.utils import secure_filename
import tensorflow_hub as hub
import tensorflow as tf
import image.utils as utils
import cv2
import numpy as np
from io import BytesIO

def get_image(path : str):
    file_path = current_app.config['UPLOAD_FOLDER'] + '/images/' + path + '.jpg';
    return send_file(file_path, mimetype=' image/jpg')

def stylized_image():
    UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads')
    content_image = request.files['content_image']
    style_image = request.files['style_image']

    content_image_filename = secure_filename(content_image.name)
    style_image_filename = secure_filename(style_image.name)

    content_image.save(os.path.join(UPLOADS_PATH, content_image_filename))
    style_image.save(os.path.join(UPLOADS_PATH, style_image_filename))

    content_image_tf = utils.load_image_from_path(os.path.join(UPLOADS_PATH, content_image_filename))
    style_image_tf = utils.load_image_from_path(os.path.join(UPLOADS_PATH, style_image_filename))

    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    stylized_image = model(tf.constant(content_image_tf), tf.constant(style_image_tf))[0]

    file_name = str(uuid.uuid4())

    image = cv2.cvtColor(np.squeeze(stylized_image) * 255, cv2.COLOR_BGR2RGB)

    return send_file(BytesIO(image), mimetype='image/jpg')
