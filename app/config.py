import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

    DISH_PRICE_ROUNDING = os.environ.get("DISH_PRICE_ROUNDING")
