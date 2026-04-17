import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
            user_id = cursor.lastrowid
            logger.info(f"Added new user with phone_number: {phone_number}, id: {user_id}")
            return user_id
    except sqlite3.IntegrityError:
        # User already exists, retrieve existing user ID
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM users WHERE phone_number = ?",
                    (phone_number,)
                )
                result = cursor.fetchone()
                if result:
                    logger.info(f"User {phone_number} already exists, returning id: {result[0]}")
                    return result[0]
                return None
        except sqlite3.Error as e:
            logger.error(f"Database error while retrieving existing user: {e}", exc_info=True)
            return None
    except sqlite3.Error as e:
        logger.error(f"Database error while adding user: {e}", exc_info=True)
        return None

def insert_reminder(user_id, task, datetime, recurrence=None, status='active'):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO reminders 
                   (user_id, task, datetime, recurrence, status) 
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, task, datetime, recurrence, status)
            )
            conn.commit()
            reminder_id = cursor.lastrowid
            logger.info(f"Inserted reminder for user {user_id}, task: '{task}', id: {reminder_id}")
            return reminder_id
    except sqlite3.Error as e:
        logger.error(f"Database error while inserting reminder: {e}", exc_info=True)
        return None

def get_active_tasks(user_id=None):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if user_id:
                cursor.execute(
                    "SELECT * FROM reminders WHERE status = 'active' AND user_id = ?",
                    (user_id,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM reminders WHERE status = 'active'"
                )
            tasks = [dict(row) for row in cursor.fetchall()]
            logger.info(f"Retrieved {len(tasks)} active tasks" + (f" for user {user_id}" if user_id else ""))
            return tasks
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching active tasks: {e}", exc_info=True)
        return []

def update_task_status(task_id, status):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reminders SET status = ? WHERE id = ?",
                (status, task_id)
            )
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Updated task {task_id} status to '{status}'.")
            else:
                logger.warning(f"Could not update task {task_id}. Task may not exist.")
            return success
    except sqlite3.Error as e:
        logger.error(f"Database error while updating task status: {e}", exc_info=True)
        return False
