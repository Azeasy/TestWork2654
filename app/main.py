from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router


app = FastAPI(title="Task Service")

app.include_router(users_router)
app.include_router(tasks_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Task Management API!"}
