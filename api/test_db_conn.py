import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Connecting to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 5})
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print(f"PostgreSQL Version: {result.fetchone()}")
        print("✅ Connection successful!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
