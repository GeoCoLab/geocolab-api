# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Facility


class FacilitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Facility

    managers = ma.List(ma.Nested('MinimalUserSchema'))
