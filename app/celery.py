from celery import Celery  # type: ignore

from app.config import Config

celery = Celery('tasks', broker=Config.RABBITMQ_URL)
