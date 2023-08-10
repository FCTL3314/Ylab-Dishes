from app.celery import celery


@celery.task()
def load_all_data():
    ...
