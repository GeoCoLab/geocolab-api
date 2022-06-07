# !/usr/bin/env python
# encoding: utf-8

from ..extensions import db


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    description = db.Column(db.String())
    parent_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=True)

    children = db.relationship('Analysis', backref=db.backref('parent', remote_side=[id]))

    def __str__(self):
        def get_hierarchy(items):
            if items[0].parent is None:
                return items
            else:
                return get_hierarchy([items[0].parent] + items)

        parents = [p.name for p in get_hierarchy([self])]
        return ' > '.join(parents)
