# !/usr/bin/env python
# encoding: utf-8

from ..extensions import db


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False, unique=True)

    fields = db.relationship('FormField', backref='form')


class FormField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    order = db.Column(db.Integer, default=1)
    field_json = db.Column(db.JSON)

    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
