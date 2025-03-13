from fastapi import FastAPI
from sqlmodel import Session
from src.database import engine
from src.seed import seed_data
from src.todo.router import router as todo_router

app = FastAPI()
app.include_router(todo_router)


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        seed_data(session)
