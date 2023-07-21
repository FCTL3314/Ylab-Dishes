from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import Config

SQLALCHEMY_URI = (
    f"postgresql://"
    f"{Config.POSTGRES_USER}:"
    f"{Config.POSTGRES_PASSWORD}@"
    f"{Config.POSTGRES_HOST}/"
    f"{Config.POSTGRES_DB}"
)
engine = create_engine(SQLALCHEMY_URI)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Depends(get_session)
