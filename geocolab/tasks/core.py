from celery import Celery

celery = Celery('geocolab', autofinalize=False)
