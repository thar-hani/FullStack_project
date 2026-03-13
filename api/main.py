from fastapi import FastAPI
import model
from db import database
from routers import user, story, todo, wish
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
def startup():
    try:
        model.Base.metadata.create_all(bind=database.engine)
    except Exception as e:
        print(f"Error creating tables: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is running successfully 🚀"}

app.include_router(user.router)
app.include_router(story.router)
app.include_router(todo.router)
app.include_router(wish.router)

