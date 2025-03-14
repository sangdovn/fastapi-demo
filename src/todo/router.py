from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.dependencies import SessionDep
from src.todo.models import Todo
from src.todo.schemas import TodoCreate

router = APIRouter(prefix="/todos", tags=["Todo"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(new_todo: TodoCreate, session: SessionDep):
    todo = Todo(**new_todo.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(session: SessionDep):
    stmt = select(Todo)
    todos = session.scalars(stmt).all()
    return todos


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo_id: int, todo_data: TodoCreate, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed
    session.add(todo)
    session.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
