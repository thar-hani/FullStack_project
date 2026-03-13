from db.database import engine
from model.user import User
from model.story import Story
from model.todo import Todo
from model.wish import Wish

print("Dropping all tables...")
Wish.__table__.drop(engine, checkfirst=True)
Todo.__table__.drop(engine, checkfirst=True)
Story.__table__.drop(engine, checkfirst=True)
User.__table__.drop(engine, checkfirst=True)

print("Recreating all tables...")
from db.database import Base
Base.metadata.create_all(bind=engine)
print("✅ Database tables recreated successfully!")
