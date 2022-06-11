import os
from datetime import timedelta

root = os.environ.get('ROOT_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def get_database_url():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url.replace('postgres://', 'postgresql+psycopg2://')
    username = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('DATABASE_HOST')
    port = os.environ.get('POSTGRES_PORT')
    database = os.environ.get('POSTGRES_DB')
    return f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'


def get_broker_url():
    broker_url = os.environ.get('RABBITMQ_URL')
    if broker_url:
        return broker_url
    username = os.environ.get('RABBITMQ_DEFAULT_USER')
    password = os.environ.get('RABBITMQ_DEFAULT_PASS')
    return f'amqp://{username}:{password}@rabbitmq:5672'


class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG', 0) == 1
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = os.environ.get('SECRET')

    JWT_SECRET_KEY = os.environ.get('SECRET')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_SESSION_COOKIE = False

    ROOT_DIR = root
    STATIC_DIR = os.environ.get('STATIC_DIR', os.path.join(root, 'static'))

    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'geocolab.app@gmail.com'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'geocolab.app@gmail.com'

    CELERY_BROKER_URL = get_broker_url()
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULTS_BACKEND', os.environ.get('REDIS_URL'))

