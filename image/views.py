from flask import request, send_file, current_app

def get_image(path : str):
    file_path = current_app.config['UPLOAD_FOLDER'] + '/images/' + path + '.jpg';
    return send_file(file_path, mimetype=' image/jpg')