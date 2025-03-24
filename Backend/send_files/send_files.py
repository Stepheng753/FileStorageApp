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
    files_dict = {}
    for root, _, files in os.walk(FILES_PATH):
        folder_name = os.path.basename(root)
        files_dict[folder_name] = files
    return files_dict