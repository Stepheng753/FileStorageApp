from flask import request
import os

def upload_file():
    if 'file' not in request.files:
        return {'status': 'failure', 'message': 'No file provided'}

    file = request.files['file']

    if file.filename == '':
        return {'status': 'failure', 'message': 'No selected file'}

    if file:
        filename = file.filename
        filepath = os.path.join('files/', filename)
        file.save(filepath)
        return {'STATUS': 'SUCCESS'}

    return  {'STATUS': 'FAILURE'}


def download_files():
    return os.listdir('./files/')