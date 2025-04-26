from flask import request, url_for
import os
from main import FILES_PATH

def upload_file():
    if 'file' not in request.files:
        return {'STATUS': 'FAILURE', 'ERROR': 'NO FILE PROVIDED'}

    file = request.files['file']
    folder = request.form['folder']

    if file.filename == '':
        return {'STATUS': 'FAILURE', 'ERROR': 'NO SELECTED FILE'}
    if folder == '':
        return {'STATUS': 'FAILURE', 'ERROR': 'No SELECTED FOLDER'}

    os.makedirs(os.path.join(FILES_PATH, folder), exist_ok=True)

    if file:
        filename = folder + '/' + file.filename
        filepath = os.path.join(FILES_PATH, filename)
        file.save(filepath)
        file_url = url_for('static', filename=filename, _external=True)
        return {'STATUS': 'SUCCESS'}

    return  {'STATUS': 'FAILURE'}


def download_files():
    files_dict = {}
    for root, _, files in os.walk(FILES_PATH):
        folder_name = os.path.basename(root)
        files_dict[folder_name] = files
    return files_dict


def delete_file():
    folder = request.form['folder']
    filename = request.form['file']
    filepath = os.path.join(FILES_PATH, folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        if not os.listdir(os.path.join(FILES_PATH, folder)):
            os.rmdir(os.path.join(FILES_PATH, folder))

        return {'STATUS': 'SUCCESS'}
    else:
        return {'STATUS': 'FAILURE', 'ERROR': 'FILE NOT FOUND'}