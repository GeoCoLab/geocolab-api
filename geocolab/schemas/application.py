# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Application


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
