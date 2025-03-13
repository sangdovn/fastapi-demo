from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TodoCreate(Todo):
    pass


class TodoUpdate(Todo):
    pass
