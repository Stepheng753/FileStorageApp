from flask import request
from main import *
from database.create_test_db import get_user, insert_user

def login():
    user_pass = request.form
    if user_pass is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in user_pass or "password" not in user_pass:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = user_pass["username"]
    password = user_pass["password"]

    users = get_user(username)

    if not users:
        return {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}

    if len(users) == 0:
        return {'STATUS': 'FAILURE', 'ERROR': 'USER NOT FOUND'}
    else:
        users = users[0]

    if users[PASSWORD_IDX] == password:
        return {'STATUS': 'SUCCESS'}
    else:
        return {'STATUS': 'FAILURE', 'ERROR': 'WRONG PASSWORD'}


def register():
    user_pass = request.form
    if user_pass is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in user_pass or "password" not in user_pass:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = user_pass["username"]
    password = user_pass["password"]

    if insert_user(username, password):
        return {'STATUS': 'SUCCESS'}
    else:
        return {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}
