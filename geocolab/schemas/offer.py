# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Offer


class OfferSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Offer
