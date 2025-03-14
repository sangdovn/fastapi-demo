from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from src.constants import DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def get_session():
    with Session() as session:
        yield session
