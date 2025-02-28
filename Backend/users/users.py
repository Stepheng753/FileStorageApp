from flask import request
from main import *
from database.sql_funcs import *

def login():
    user_pass = request.form
    if user_pass is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in user_pass or "password" not in user_pass:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = user_pass["username"]
    password = user_pass["password"]

    user = get_user_entry(username)

    if not user:
        return {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}

    login_success = user[PASSWORD_IDX] == password
    return {'STATUS': 'SUCCESS'} if login_success else {'STATUS': 'FAILURE', 'ERROR': 'WRONG PASSWORD'}


def register():
    user_pass = request.form
    if user_pass is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in user_pass or "password" not in user_pass:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = user_pass["username"]
    password = user_pass["password"]

    register_success = insert_user_entry(username, password)
    return {'STATUS': 'SUCCESS'} if register_success else {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}


def update_permission_tier():
    user_permission = request.form
    if user_permission is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in user_permission or "permission_tier" not in user_permission:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = user_permission["username"]
    permission_tier = user_permission["permission_tier"]

    update_success = update_user_entry_permission(username, permission_tier)
    return {'STATUS': 'SUCCESS'} if update_success else {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}


def update_password():
    user_old_new_pass = request.form
    print(user_old_new_pass)
    if user_old_new_pass is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in user_old_new_pass or \
            "old_password" not in user_old_new_pass or \
            "new_password" not in user_old_new_pass:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = user_old_new_pass["username"]
    old_password = user_old_new_pass["old_password"]
    new_password = user_old_new_pass["new_password"]

    user = get_user_entry(username)
    if user[PASSWORD_IDX] != old_password:
        return {'STATUS': 'FAILURE', 'ERROR': 'PAST PASSWORD NOT CORRECT'}

    update_success = update_user_entry_password(username, new_password)
    return {'STATUS': 'SUCCESS'} if update_success else {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}


def get_user():
    username_entry = request.form
    if username_entry is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in username_entry:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = username_entry["username"]
    user = get_user_entry(username)
    return [user] if user else {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}


def get_all_users():
    all_users = get_all_users_entries()
    return all_users if all_users else {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}


def delete_user():
    user = request.form
    if user is None:
        return {'STATUS': 'FAILURE', 'ERROR': 'INVALID RESPONSE'}, 400
    if "username" not in user:
        return {'STATUS': 'FAILURE', 'ERROR': 'MISSING PARAMETERS'}, 400
    username = user["username"]

    delete_success = delete_user_entry(username)
    return {'STATUS': 'SUCCESS'} if delete_success else {'STATUS': 'FAILURE', 'ERROR': 'DB ERROR'}
