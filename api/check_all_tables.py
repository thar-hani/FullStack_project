from db.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = ['users', 'stories', 'todos', 'wishes']

for table in tables:
    columns = [c['name'] for c in inspector.get_columns(table)]
    print(f"{table}: {columns}")
