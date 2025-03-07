#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from main import *
from users.users import *
from send_files.send_files import *

app = Flask(__name__)
CORS(app)

app.add_url_rule("/", "index", index)
app.add_url_rule("/login", "login", login, methods=["POST"])
app.add_url_rule("/register", "register", register, methods=["POST"])

app.add_url_rule("/upload_file", "upload_file", upload_file, methods=["POST"])
app.add_url_rule("/download_files", "download_files", download_files, methods=["POST"])

app.add_url_rule("/update_permission_tier", "update_permission_tier", update_permission_tier, methods=["POST"])
app.add_url_rule("/update_password", "update_password", update_password, methods=["POST"])
app.add_url_rule("/get_user", "get_user", get_user, methods=["POST"])
app.add_url_rule("/get_all_users", "get_all_users", get_all_users, methods=["GET"])
app.add_url_rule("/delete_user", "delete_user", delete_user, methods=["POST"])

app.add_url_rule("/get_key", "get_key", get_key, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)