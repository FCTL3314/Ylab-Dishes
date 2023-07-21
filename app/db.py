from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import Config

engine = create_engine(Config.SQLALCHEMY_URI)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Depends(get_session)
