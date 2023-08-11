from celery import Celery  # type: ignore

from app.config import Config

celery = Celery(
    __name__,
    broker=Config.RABBITMQ_AMQP_URL,
    backend=Config.RABBITMQ_RPC_URL,
    include=['app.data_processing.tasks'],
)
