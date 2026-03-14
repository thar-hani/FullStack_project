from fastapi import FastAPI
from api import model
from api.db import database
from api.routers import user, story, todo, wish
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        if database.engine:
            model.Base.metadata.create_all(bind=database.engine)
    except Exception as e:
        print("Database initialization failed:", e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
def root():
    return {"message": "API is running successfully"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(user.router, prefix="/api")
app.include_router(story.router, prefix="/api")
app.include_router(todo.router, prefix="/api")
app.include_router(wish.router, prefix="/api")