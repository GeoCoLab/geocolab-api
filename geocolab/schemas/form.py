# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import Form, FormField
from .fields import SortedPluck
from marshmallow import pre_load


class FormFieldSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FormField

    @pre_load
    def transform_load(self, data, **kwargs):
        name = data.get('name')
        return {'name': name, 'field_json': data}


class FormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Form

    fields = SortedPluck('FormFieldSchema', 'field_json', many=True)
