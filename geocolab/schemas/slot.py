# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Slot


class SlotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Slot
