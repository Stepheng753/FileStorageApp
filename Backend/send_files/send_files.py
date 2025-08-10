from flask import request, url_for
import os
import shutil
from main import FILES_PATH

def upload_file():
    folder = request.form['folder']
    if folder == '':
        return {'STATUS': 'FAILURE', 'ERROR': 'No SELECTED FOLDER'}

    os.makedirs(os.path.join(FILES_PATH, folder), exist_ok=True)

    files = request.files.getlist('file')
    if not files or all(f.filename == '' for f in files):
        return {'STATUS': 'SUCCESS'}

    print('Received files:', [f.filename for f in files])  # Debug log
    for file in files:
        if file and file.filename != '':
            filename = folder + '/' + file.filename
            filepath = os.path.join(FILES_PATH, filename)
            file.save(filepath)

    return {'STATUS': 'SUCCESS'}


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