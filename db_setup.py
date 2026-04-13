import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_database():
    try:
        with sqlite3.connect('assistant.db') as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create reminders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    task TEXT NOT NULL,
                    datetime TEXT NOT NULL,
                    recurrence TEXT,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create scheduled_messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scheduled_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    recipient_number TEXT NOT NULL,
                    message TEXT NOT NULL,
                    time TEXT NOT NULL,
                    recurrence TEXT,
                    last_sent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
        logger.info("Database `assistant.db` setup completed successfully.")
    except sqlite3.Error as e:
        logger.error(f"An error occurred while setting up the database: {e}", exc_info=True)

if __name__ == '__main__':
    setup_database()
