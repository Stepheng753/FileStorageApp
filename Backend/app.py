#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from main import *
from login.login import *
from upload.upload import *

app = Flask(__name__)
CORS(app)

app.add_url_rule("/", "index", index)
app.add_url_rule("/get_user_pass", "get_user_pass", get_user_pass, methods=["POST"])
app.add_url_rule("/upload_file", "upload_file", upload_file, methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True)