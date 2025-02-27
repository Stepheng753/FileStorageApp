#!/usr/bin/env python3

import sqlite3

def create_file_database():
    try:
        conn = sqlite3.connect('file_database.db')
        cursor = conn.cursor()
        command_create_table = """
            CREATE TABLE IF NOT EXISTS
            files(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                filename TEXT NOT NULL,
                filetype TEXT NOT NULL,
                size INTEGER NOT NULL
            ) """
        cursor.execute(command_create_table)

        cursor.execute('''INSERT INTO files (user_id, filename, filetype, size)
                          VALUES (1, 'example.txt', 'text/plain', 1024)''')

        conn.commit()
        conn.close()
        print("Database created successfully")

    except sqlite3.Error as e:
        print(e)
        print("Error creating database")
        return False
    return True

if __name__ == "__main__":
    create_file_database()