# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Analysis


class AnalysisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Analysis

    parent = ma.Pluck('AnalysisSchema', 'id')
    children = ma.List(ma.Pluck('AnalysisSchema', 'id'))


class NestedAnalysisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Analysis

    children = ma.List(ma.Nested('NestedAnalysisSchema'))
