# !/usr/bin/env python
# encoding: utf-8

from flask_jwt_extended import current_user
from ..extensions import db
from .utils import countries_enum


class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    country = db.Column(countries_enum)
    ror_id = db.Column(db.String(9), index=True)

    facilities = db.relationship('Facility', backref='org')

    def can_edit(self, user=None):
        user = user or current_user
        if user.is_admin:
            return True
        else:
            return user.id in [u.id for u in self.managers]
