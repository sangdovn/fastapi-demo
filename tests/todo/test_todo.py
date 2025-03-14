from sqlalchemy import text
from src.todo.models import Todo
from fastapi import status
from fastapi.testclient import TestClient
import pytest
from tests.utils import Session, client


@pytest.fixture
def test_todo():
    with Session() as session:
        session.execute(
            text("DELETE FROM todos;")
        )  # Clear todos before creating a new one
        todo = Todo(
            title="Buy groceries",
            description="Milk, Eggs, Bread",
            completed=False,
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        yield todo
    with Session() as session:
        session.execute(text("DELETE FROM todos;"))  # Clean up after the test run
        session.commit()


def test_create_todo():
    new_todo_data = {
        "title": "Buy groceries",
        "description": "Milk, Eggs, Bread",
        "completed": False,
    }
    response = client.post("/todos/", json=new_todo_data)
    session = Session()
    db_todo = session.get(Todo, response.json()["id"])
    assert response.status_code == status.HTTP_201_CREATED
    assert db_todo.title == new_todo_data["title"]
    assert db_todo.description == new_todo_data["description"]
    assert db_todo.completed == new_todo_data["completed"]
    # Assert the length of the database
    assert len(session.query(Todo).all()) == 1


def test_read_all_todos(test_todo):
    response = client.get("/todos/")
    print(f"response.json() {response.json()}")  # Log the response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": test_todo.id,
            "title": test_todo.title,
            "description": test_todo.description,
            "completed": test_todo.completed,
        }
    ]


def test_update_todo(test_todo):
    response = client.put(
        f"/todos/{test_todo.id}",
        json={
            "title": "Buy groceries and more",
            "description": "Milk, Eggs, Bread, Butter",
            "completed": True,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    session = Session()
    updated_todo = session.get(Todo, test_todo.id)
    assert updated_todo.title == "Buy groceries and more"
    assert updated_todo.description == "Milk, Eggs, Bread, Butter"
    assert updated_todo.completed is True


def test_delete_todo(test_todo):
    response = client.delete(f"/todos/{test_todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    session = Session()
    deleted_todo = session.get(Todo, test_todo.id)
    assert deleted_todo is None  # Check if the todo no longer exists in the database

    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_read_todo(test_todo):
    response = client.get(f"/todos/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK

    session = Session()
    db_todo = session.get(Todo, test_todo.id)
    assert db_todo.id == test_todo.id
    assert db_todo.title == test_todo.title
    assert db_todo.description == test_todo.description
    assert db_todo.completed is test_todo.completed


def test_update_todo_not_found():
    response = client.put(
        "/todos/999",
        json={
            "title": "Non-existent todo",
            "description": "This should not work",
            "completed": False,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_read_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_read_todo_not_found():
    response = client.get("/todos/999")  # Assuming 999 does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
