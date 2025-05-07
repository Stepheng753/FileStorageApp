#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
from main import *
from users.users import *
from send_files.send_files import *

app = Flask(__name__, static_folder="static")
CORS(app, origins=["http://toothmanager.com"], supports_credentials=True)

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type',
               'Test-Header': 'Test-Value'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

app.add_url_rule("/", "index", index)
app.add_url_rule("/login", "login", login, methods=["POST"])
app.add_url_rule("/register", "register", register, methods=["POST"])

app.add_url_rule("/upload_file", "upload_file", upload_file, methods=["POST"])
app.add_url_rule("/download_files", "download_files", download_files, methods=["POST"])
app.add_url_rule("/delete_file", "delete_file", delete_file, methods=["POST"])

app.add_url_rule("/update_permission_tier", "update_permission_tier", update_permission_tier, methods=["POST"])
app.add_url_rule("/update_password", "update_password", update_password, methods=["POST"])
app.add_url_rule("/get_user", "get_user", get_user, methods=["POST"])
app.add_url_rule("/get_all_users", "get_all_users", get_all_users, methods=["GET"])
app.add_url_rule("/delete_user", "delete_user", delete_user, methods=["POST"])

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="69.62.71.85", debug=False)