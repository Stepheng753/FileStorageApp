import sqlite3
from typing import Optional, List, Dict, Any
from core.config import DB_PATH
from core.security import is_legacy_plaintext, hash_password


def get_connection() -> sqlite3.Connection:
    """Create a connection with sqlite3.Row row factory for dict-like access."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Ensure database and required tables exist with proper constraints."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                permission_tier INTEGER NOT NULL DEFAULT 3,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)')
        conn.commit()


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Retrieve user record by username (case-insensitive lookup)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, firstname, lastname, username, password, permission_tier, created_at
            FROM users
            WHERE UPPER(username) = ?
        ''', (username.strip().upper(),))
        row = cursor.fetchone()
        if not row:
            return None
        return dict(row)


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user record by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, firstname, lastname, username, password, permission_tier, created_at
            FROM users
            WHERE id = ?
        ''', (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return dict(row)


def create_user(
    firstname: str,
    lastname: str,
    username: str,
    password_hash: str,
    permission_tier: int = 3
) -> Optional[Dict[str, Any]]:
    """Create a new user entry in the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (firstname, lastname, username, password, permission_tier)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                firstname.strip().capitalize(),
                lastname.strip().capitalize(),
                username.strip().upper(),
                password_hash,
                permission_tier
            ))
            conn.commit()
            new_id = cursor.lastrowid
            return get_user_by_id(new_id)
    except sqlite3.IntegrityError:
        return None
    except Exception as e:
        print(f"[DB ERROR] Failed to create user: {e}")
        return None


def get_all_users(include_passwords: bool = False) -> List[Dict[str, Any]]:
    """Get all users. By default, never return password hashes!"""
    with get_connection() as conn:
        cursor = conn.cursor()
        if include_passwords:
            cursor.execute('''
                SELECT id, firstname, lastname, username, password, permission_tier, created_at
                FROM users
                ORDER BY permission_tier ASC, firstname ASC
            ''')
        else:
            cursor.execute('''
                SELECT id, firstname, lastname, username, permission_tier, created_at
                FROM users
                ORDER BY permission_tier ASC, firstname ASC
            ''')
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def update_user_permission(username: str, permission_tier: int) -> bool:
    """Update a user's permission tier."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET permission_tier = ?
            WHERE UPPER(username) = ?
        ''', (permission_tier, username.strip().upper()))
        conn.commit()
        return cursor.rowcount > 0


def update_user_password(username: str, new_password_hash: str) -> bool:
    """Update a user's password with a new hash."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET password = ?
            WHERE UPPER(username) = ?
        ''', (new_password_hash, username.strip().upper()))
        conn.commit()
        return cursor.rowcount > 0


def delete_user_by_username(username: str) -> bool:
    """Delete a user by username."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users
            WHERE UPPER(username) = ?
        ''', (username.strip().upper(),))
        conn.commit()
        return cursor.rowcount > 0


def auto_migrate_plaintext_passwords():
    """Check database for any un-hashed legacy passwords and migrate them safely."""
    try:
        users = get_all_users(include_passwords=True)
        for user in users:
            stored = user.get("password")
            if stored and is_legacy_plaintext(stored):
                new_hash = hash_password(stored)
                update_user_password(user["username"], new_hash)
                print(f"[MIGRATION] Transparently upgraded password for user {user['username']}")
    except Exception as e:
        print(f"[MIGRATION WARNING] auto_migrate_plaintext_passwords: {e}")
