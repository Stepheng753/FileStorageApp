from flask import request, url_for
import os
import shutil
from main import FILES_PATH

def upload_file():
    if 'file' not in request.files:
        return {'STATUS': 'FAILURE', 'ERROR': 'NO FILE PROVIDED'}

    file = request.files['file']
    folder = request.form['folder']

    if not file or file.filename == '':
        os.makedirs(os.path.join(FILES_PATH, folder), exist_ok=True)
        return {'STATUS': 'SUCCESS'}
    if folder == '':
        return {'STATUS': 'FAILURE', 'ERROR': 'No SELECTED FOLDER'}

    os.makedirs(os.path.join(FILES_PATH, folder), exist_ok=True)

    if file:
        filename = folder + '/' + file.filename
        filepath = os.path.join(FILES_PATH, filename)
        file.save(filepath)
        return {'STATUS': 'SUCCESS'}

    return  {'STATUS': 'FAILURE'}


def get_folder_dict(path):
    folder_dict = {}
    for entry in os.scandir(path):
        if entry.is_dir():
            folder_dict[entry.name] = get_folder_dict(entry.path)
        elif entry.is_file():
            folder_dict.setdefault('files', []).append(entry.name)
    return folder_dict


def download_files():
    return get_folder_dict(FILES_PATH)


def delete_file():
    folder = request.form['folder']
    filename = request.form['file']
    filepath = os.path.join(FILES_PATH, folder, filename)

    if os.path.exists(filepath):
        if len(filename) > 0:
            os.remove(filepath)
        else:
            shutil.rmtree(filepath)
        return {'STATUS': 'SUCCESS'}
    else:
        return {'STATUS': 'FAILURE', 'ERROR': 'FILE NOT FOUND'}