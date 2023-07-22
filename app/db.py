from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import Config

SQLALCHEMY_URI = (
    f"postgresql://"
    f"{Config.DATABASE_USER}:"
    f"{Config.DATABASE_PASSWORD}@"
    f"{Config.DATABASE_HOST}/"
    f"{Config.DATABASE_NAME}"
)
engine = create_engine(SQLALCHEMY_URI)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Depends(get_session)
