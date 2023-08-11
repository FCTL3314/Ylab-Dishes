from datetime import timedelta

from celery import Celery  # type: ignore

from app.config import Config

celery = Celery(
    __name__,
    include=[
        'app.data_processing.tasks',
        'app.common.tasks',
    ],
)

celery.conf.broker_url = Config.RABBITMQ_AMQP_URL
celery.conf.result_backend = Config.RABBITMQ_RPC_URL
celery.conf.beat_schedule = {
    'database_synchronization': {
        'task': 'app.common.tasks.database_synchronization',
        'schedule': timedelta(seconds=15),
    },
}
