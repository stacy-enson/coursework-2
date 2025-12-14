import sqlite3
import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user


def register_user(username, password, role='user'):
    """
    Register new user with password hashing.
    Safely handles duplicate usernames.
    """
    # Check if user already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return False, f"User '{username}' already exists."

    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    try:
        insert_user(username, password_hash, role)
        return True, f"User '{username}' registered successfully."
    except sqlite3.IntegrityError:
        # Safety net (should not normally happen due to pre-check)
        return False, f"User '{username}' already exists."


def login_user(username, password):
    """
    Authenticate user.
    """
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    return False, "Incorrect password."


def migrate_users_from_file(filepath=Path("DATA") / "users.txt"):
    """
    Migrate users from users.txt into the database.
    Ignores users that already exist.
    """
    if not filepath.exists():
        print("No users.txt file found — skipping migration.")
        return 0

    conn = connect_database()
    cursor = conn.cursor()
    migrated = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) < 2:
                continue

            username = parts[0]
            password_hash = parts[1]
            role = parts[2] if len(parts) > 2 else "user"

            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
                if cursor.rowcount > 0:
                    migrated += 1
            except sqlite3.Error as e:
                print(f"Error migrating {username}: {e}")

    conn.commit()
    conn.close()
    return migrated
