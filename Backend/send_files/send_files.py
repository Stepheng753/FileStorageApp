from flask import request
import os
from main import FILES_PATH

def upload_file():
    if 'file' not in request.files:
        return {'status': 'failure', 'message': 'No file provided'}

    file = request.files['file']

    if file.filename == '':
        return {'status': 'failure', 'message': 'No selected file'}

    if file:
        filename = file.filename
        filepath = os.path.join(FILES_PATH, filename)
        file.save(filepath)
        return {'STATUS': 'SUCCESS'}

    return  {'STATUS': 'FAILURE'}


def download_files():
    return os.listdir(FILES_PATH)