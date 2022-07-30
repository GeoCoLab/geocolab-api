# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import User
from marshmallow import EXCLUDE


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password']
        unknown = EXCLUDE

    name = ma.Str()
    todo = ma.List(ma.Str)
    all_tasks = ma.List(ma.Str)
    gravatar = ma.Str()
    completion = ma.Integer()
    author = ma.Nested('BlogAuthorSchema')


class MinimalUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    name = ma.Str()
    id = ma.Integer()
