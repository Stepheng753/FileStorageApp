#!/usr/bin/env python3

import sqlite3
from main import *

def create_users_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS
            users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                permission_tier INT NOT NULL DEFAULT 2,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            ) ''')
        conn.commit()
        conn.close()
        print("DATABASE CREATED: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("DATABASE CREATED: FAILURE")
        return False

    return True


def insert_user_entry(firstname, lastname, username, password, permission_tier = 3):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (firstname, lastname, username, password, permission_tier)
            VALUES (?, ?, ?, ?, ?)
        ''', (firstname.capitalize(), lastname.capitalize(), username.upper(), password, permission_tier))
        conn.commit()
        conn.close()
        print("USER CREATED: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("USER CREATED: FAILURE")
        conn.close()
        return False

    return True


def get_user_entry(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM users
            WHERE username = ?
        ''', (username.upper(), ))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user is None:
            raise Exception("User not found")

        print("USER SELECTED: SUCCESS")

    except (sqlite3.Error, Exception) as e:
        print(e)
        print("USER SELECTED: FAILURE")
        return False

    return user


def get_all_users_entries():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM users
        ''')
        users = cursor.fetchall()
        conn.commit()
        conn.close()
        print("USERS SELECTED: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("USERS SELECTED: FAILURE")
        conn.close()
        return False

    return users


def delete_user_entry(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE
            FROM users
            WHERE username = ?
        ''', (username.upper(), ))
        conn.commit()
        conn.close()
        print("USER DELETED: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("USER DELETED: FAILURE")
        conn.close()
        return False

    return True


def delete_all_users_entries():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users
        ''')
        conn.commit()
        conn.close()
        print("USERS DELETED: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("USERS DELETED: FAILURE")
        conn.close()
        return False

    return True


def update_user_entry_permission(username, permission_tier):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET permission_tier = ?
            WHERE username = ?
        ''', (permission_tier, username.upper()))
        conn.commit()
        conn.close()
        print("USER UPDATED PERMISSION: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("USER UPDATED PERMISSION: FAILURE")
        conn.close()
        return False

    return True


def update_user_entry_password(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET password = ?
            WHERE username = ?
        ''', (password, username.upper()))
        conn.commit()
        conn.close()
        print("USER UPDATED PASSWORD: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("USER UPDATED PASSWORD: FAILURE")
        conn.close()
        return False

    return True
