from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.constants import DATABASE_URL_TEST
from src.database import Base, get_session
from fastapi.testclient import TestClient
from src.main import app

engine = create_engine(DATABASE_URL_TEST, echo=True)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_session():
    with Session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)
