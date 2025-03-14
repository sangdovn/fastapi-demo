from fastapi import FastAPI
from src.todo.router import router as todo_router

app = FastAPI()
app.include_router(todo_router)


@app.get("/health")
def health():
    return {"status": "ok"}
