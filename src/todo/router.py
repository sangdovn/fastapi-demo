from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from src.dependencies import SessionDep
from src.todo.models import Todo
from src.todo.schemas import TodoCreate, TodoUpdate

router = APIRouter(prefix="/todos", tags=["Todo"])


@router.post("/", status_code=201)
async def create_todo(new_todo: TodoCreate, session: SessionDep):
    todo = Todo(**new_todo.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.get("/", status_code=200)
async def read_all_todos(session: SessionDep):
    statement = select(Todo)
    todos = session.exec(statement).all()
    return todos


@router.get("/{todo_id}", status_code=200)
async def read_todo(todo_id: int, session: SessionDep):
    statement = select(Todo).where(Todo.id == todo_id)
    todo = session.exec(statement).one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", status_code=204)
async def update_todo(todo_id: int, todo_data: TodoCreate, session: SessionDep):
    statement = select(Todo).where(Todo.id == todo_id)
    todo = session.exec(statement).one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed
    session.add(todo)
    session.commit()
    session.refresh(todo)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, session: SessionDep):
    statement = select(Todo).where(Todo.id == todo_id)
    todo = session.exec(statement).one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
