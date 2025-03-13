from sqlmodel import create_engine, SQLModel, Session
from src.constants import DATABASE_URL

# Create a database engine with the specified URL and enable echo for logging
engine = create_engine(DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)


# Function to get a database session
def get_session():
    # Use a context manager to ensure the session is properly closed after use
    with Session(engine) as session:
        yield session  # Yield the session for use in a context
