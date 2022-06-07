# !/usr/bin/env python
# encoding: utf-8

from marshmallow.fields import Pluck


class SortedPluck(Pluck):
    def _serialize(self, nested_obj, attr, obj, **kwargs):
        nested_obj = sorted(nested_obj, key=lambda x: x.order)
        return super(SortedPluck, self)._serialize(nested_obj, attr, obj, **kwargs)
