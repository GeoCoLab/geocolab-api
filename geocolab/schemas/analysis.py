# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Analysis


class AnalysisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Analysis
