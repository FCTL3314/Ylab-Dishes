import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

    DISH_PRICE_ROUNDING = os.environ.get("DISH_PRICE_ROUNDING")
