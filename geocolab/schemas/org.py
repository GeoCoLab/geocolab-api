# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Org


class OrgSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Org
