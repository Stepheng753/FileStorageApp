import sqlite3

def insert_file(filename, filetype, size, user_id):
    try:
        conn = sqlite3.connect('file_database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO files (user_id, filename, filetype, size)
            VALUES (?, ?, ?, ?)
        ''', (user_id, filename, filetype, size))
        conn.commit()
        conn.close()
        print("File inserted successfully")

    except sqlite3.Error:
        print("Error inserting file")
        return False
    return True