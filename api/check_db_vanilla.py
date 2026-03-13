import sqlite3
import os

db_path = 'journal.db'
if not os.path.exists(db_path):
    # Try looking in parent or child dirs if not found
    print(f"File {db_path} not found in current directory.")
    # Add logic to find it if needed, but usually it's in Backend/
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        for table in tables:
            t_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {t_name}")
            count = cursor.fetchone()[0]
            print(f"Table {t_name}: {count} rows")
            if t_name == 'users' and count > 0:
                cursor.execute("SELECT id, full_name, emailID FROM users")
                print(f"Users: {cursor.fetchall()}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
