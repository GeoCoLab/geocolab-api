# !/usr/bin/env python
# encoding: utf-8


from .mixins import UserDataMixin
from ..utils import countries_enum
from ...extensions import db


class EDIData(UserDataMixin, db.Model):
    NAME = 'edi'

    country = db.Column(db.Boolean)
    country_expand = db.Column(countries_enum)
    gender = db.Column(db.String(100))
    gender_expand = db.Column(db.String(200))
    trans = db.Column(db.String(50))
    orientation = db.Column(db.String(100))
    orientation_expand = db.Column(db.String())
    ethnicity = db.Column(db.String(100))
    ethnicity_expand = db.Column(db.String())
    disability = db.Column(db.String(100))
    disability_expand = db.Column(db.String())


class EDIExtraData(UserDataMixin, db.Model):
    NAME = 'edi_extra'

    role_type = db.Column(db.String(50))
    role_type_expand = db.Column(db.String())
    career_stage = db.Column(db.String(50))
    contract = db.Column(db.String(50))
    funding = db.Column(db.String(50))
    funding_expand = db.Column(db.String())
    has_budget = db.Column(db.Boolean)
    budget_value = db.Column(db.Integer)
    budget_currency = db.Column(db.String)
    family_firsts = db.Column(db.JSON)
