from sqlmodel import select
from src.todo.models import Todo
from src.dependencies import SessionDep


def seed_data(session: SessionDep):
    statement = select(Todo)
    todos = session.exec(statement).all()
    if not todos:  # Simplified check for empty list
        todos = [
            Todo(
                title="Buy groceries",
                description="Milk, Eggs, Bread",
                completed=False,
            ),
            Todo(
                title="Clean the house",
                description="Vacuum and dust all rooms",
                completed=False,
            ),
            Todo(
                title="Finish homework",
                description="Complete math and science assignments",
                completed=False,
            ),
            Todo(
                title="Walk the dog",
                description="Take the dog for a walk in the park",
                completed=False,
            ),
            Todo(
                title="Read a book",
                description="Finish reading 'The Great Gatsby'",
                completed=False,
            ),
            Todo(
                title="Exercise",
                description="Go for a run or do a workout",
                completed=False,
            ),
            Todo(
                title="Call mom",
                description="Check in with mom and see how she's doing",
                completed=False,
            ),
            Todo(
                title="Prepare dinner",
                description="Cook a healthy meal for the family",
                completed=False,
            ),
            Todo(
                title="Plan vacation",
                description="Research and plan the next family vacation",
                completed=False,
            ),
            Todo(
                title="Organize closet",
                description="Sort through clothes and donate what I don't need",
                completed=False,
            ),
        ]
        session.add_all(todos)  # Moved add_all inside the if block
        session.commit()  # Commit only if new todos are added
        for todo in todos:
            session.refresh(todo)
