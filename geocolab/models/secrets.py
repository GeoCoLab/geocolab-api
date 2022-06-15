# !/usr/bin/env python
# encoding: utf-8

from ..extensions import db, crypt


class Secret(db.Model):
    key = db.Column(db.String(50), index=True, primary_key=True)
    value = db.Column(db.String)

    def value_set(self, plaintext):
        self.value = crypt.hash(plaintext)

    def value_verify(self, plaintext):
        return crypt.verify(plaintext, self.value)
