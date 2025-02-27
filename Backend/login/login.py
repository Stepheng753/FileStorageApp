from flask import request

def get_user_pass():
    user_pass = request.form
    if user_pass is None:
        return {"status": "failure", "error": "Invalid request"}, 400
    if "username" not in user_pass or "password" not in user_pass:
        return {"status": "failure", "error": "Missing parameters"}, 400
    username = user_pass["username"]
    password = user_pass["password"]
    print(username, password)
    return {"status": "success"}