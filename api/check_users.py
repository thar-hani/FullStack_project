from sqlalchemy import create_client
import sqlite3

# Simple sqlite3 check since it's likely a local sqlite db
try:
    conn = sqlite3.connect('journal.db') # Assuming name from standard FastAPI tutorials or looking at folders
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    if ('users',) in tables:
        cursor.execute("SELECT id, full_name, emailID FROM users")
        users = cursor.fetchall()
        print(f"Users: {users}")
    conn.close()
except Exception as e:
    print(f"Error checking DB: {e}")
