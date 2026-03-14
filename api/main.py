from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api import model
from api.db import database
from api.routers import user, story, todo, wish
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error_message": str(exc), "error_type": type(exc).__name__}
    )

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