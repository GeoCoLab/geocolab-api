# !/usr/bin/env python
# encoding: utf-8

from ..extensions import db
from flask_jwt_extended import current_user


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    notes = db.Column(db.String)
    other_analyses = db.Column(db.String)
    org_id = db.Column(db.Integer, db.ForeignKey('org.id'), nullable=False)

    _analyses = db.relationship('Analysis', secondary='facility_analyses', backref=db.backref('facilities', lazy=True),
                                lazy=True)
    slots = db.relationship('Slot', backref='facility')

    @property
    def managers(self):
        return [m for m in self._managers] + self.org.managers

    @property
    def analyses(self):
        def get_children(analysis):
            if len(analysis.children) > 0:
                for child in analysis.children:
                    for subchild in get_children(child):
                        yield subchild
            else:
                yield analysis

        return [child for analysis in self._analyses for child in get_children(analysis)]

    @property
    def open_slots(self):
        return [s for s in self.slots if s.is_open]

    @property
    def closed_slots(self):
        return [s for s in self.slots if not s.is_open]

    @property
    def can_edit(self):
        if not current_user:
            return False
        elif current_user.is_admin:
            return True
        else:
            return current_user.id in [u.id for u in self.managers]

    def via(self, user):
        if self.id in [f.id for f in user._facilities]:
            return
        elif self.org_id in [o.id for o in user.managed_orgs]:
            return self.org.name
        elif user.is_admin:
            return 'administrator role'
        else:
            raise PermissionError('This should not happen.')

