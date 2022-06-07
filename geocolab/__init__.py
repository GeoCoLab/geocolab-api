# !/usr/bin/env python
# encoding: utf-8

from flask import Flask

from . import tasks, utils
from .config import Config
from .extensions import db, migrate, jwt_manager, mail, ma


def init(return_celery=False):
    app = Flask(__name__, static_folder=Config.STATIC_DIR,
                static_url_path='/static/')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    mail.init_app(app)
    celery = tasks.init_app(app)
    utils.init_app(app)
    ma.init_app(app)

    from . import routes, models
    routes.init_app(app)

    return celery if return_celery else app


def create_app():
    return init()


def create_celery():
    return init(return_celery=True)
