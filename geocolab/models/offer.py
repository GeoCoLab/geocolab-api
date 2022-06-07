# !/usr/bin/env python
# encoding: utf-8
from ..extensions import db
from datetimerange import DateTimeRange


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

    slot = db.relationship('Slot', backref='offers')
    application = db.relationship('Application', backref=db.backref('offer', uselist=False))

    @property
    def range(self):
        return DateTimeRange(self.date_from, self.date_to)

    def precedes(self, other):
        return (other - self.date_to).days == 1

    def follows(self, other):
        return (self.date_from - other).days == 1

    def adjacent(self, other):
        return self.precedes(other) or self.follows(other)

    def contains(self, date):
        return date in self.range
