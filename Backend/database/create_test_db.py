#!/usr/bin/env python3

import sqlite3
import os
from main import *

def create_users_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS
            users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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
        conn.close()
        return False

    return True


def insert_user(username, password, permission_tier = 2):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, permission_tier)
            VALUES (?, ?, ?)
        ''', (username.upper(), password, permission_tier))
        conn.commit()
        conn.close()
        print("USER CREATED: SUCCESS")

    except sqlite3.Error as e:
        print(e)
        print("USER CREATED: FAILURE")
        conn.close()
        return False

    return True


def get_user(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM users
            WHERE username = ?
        ''', (username.upper(), ))
        users = cursor.fetchall()
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(e)
        print("USER SELECTED: FAILURE")
        conn.close()
        return False

    return users


def get_all_users():
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

    except sqlite3.Error as e:
        print(e)
        print("USER SELECTED: FAILURE")
        conn.close()
        return False

    return users


def delete_all_users():
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
        print("USER DELETED: FAILURE")
        conn.close()
        return False

    return True


def test_insert_get_users():
    insert_user("Test4", "Test2Pass", 2)
    print(get_all_users())