import os

def download_files():
    files = os.listdir('./files/')
    print(files)
    return {'files': files}