from sqlmodel import SQLModel, Field


# Define the Todo model, which represents a task in the to-do list
class Todo(SQLModel, table=True):
    __tablename__ = "todos"  # Specify the name of the database table

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
