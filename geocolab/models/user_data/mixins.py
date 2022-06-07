# !/usr/bin/env python
# encoding: utf-8

from ...extensions import db
from sqlalchemy.orm import backref, declared_attr, declarative_mixin


class UserDataMixin(object):
    NAME = 'userdata'
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    @declared_attr
    def form_id(cls):
        return db.Column(db.Integer, db.ForeignKey('form.id'))

    @declared_attr
    def user(cls):
        return db.relationship('User', backref=backref(cls.NAME, uselist=False))
