import sqlite3

DB_NAME = 'assistant.db'

def add_user(phone_number):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (phone_number) VALUES (?)",
                (phone_number,)
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        # User already exists, retrieve existing user ID
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE phone_number = ?",
                (phone_number,)
            )
            result = cursor.fetchone()
            return result[0] if result else None

def insert_reminder(user_id, task, datetime, recurrence=None, status='pending'):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO reminders 
               (user_id, task, datetime, recurrence, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, task, datetime, recurrence, status)
        )
        conn.commit()
        return cursor.lastrowid

def get_active_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reminders WHERE status = 'pending'"
        )
        return [dict(row) for row in cursor.fetchall()]

def update_task_status(task_id, status):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reminders SET status = ? WHERE id = ?",
            (status, task_id)
        )
        conn.commit()
        return cursor.rowcount > 0
