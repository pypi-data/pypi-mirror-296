from typing import Tuple
from datetime import timedelta
import sqlite3

DATABASE_FILE = 'timedelta.db'

def setup_database():
    """Sets up the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS timedeltas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        weeks INTEGER,
        days INTEGER,
        hours INTEGER,
        minutes INTEGER,
        seconds INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def save_timedelta(description: str, td: timedelta):
    """Saves a timedelta object to the database with a description."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Convert timedelta to components
    total_seconds = int(td.total_seconds())
    weeks, remainder = divmod(total_seconds, 7 * 24 * 3600)
    days, remainder = divmod(remainder, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    cursor.execute('''
    INSERT INTO timedeltas (description, weeks, days, hours, minutes, seconds)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (description, weeks, days, hours, minutes, seconds))
    
    conn.commit()
    conn.close()

def load_timedelta(id: int) -> Tuple[timedelta, str]:
    """Loads a timedelta object from the database by ID."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT description, weeks, days, hours, minutes, seconds FROM timedeltas WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        description, weeks, days, hours, minutes, seconds = row
        total_seconds = (
            (weeks * 7 * 24 * 3600) +
            (days * 24 * 3600) +
            (hours * 3600) +
            (minutes * 60) +
            seconds
        )
        return timedelta(seconds=total_seconds), description
    else:
        print(f"No data found for ID {id}.")
        raise ValueError("No timedelta found with the given ID")
