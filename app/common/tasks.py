from app.celery import celery


@celery.task
def database_synchronization():
    print('Not implemented...')
