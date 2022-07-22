from sqlalchemy.sql import func

from .utils import countries_enum, user_types_enum, gravatar
from ..extensions import db, crypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    given_name_first = db.Column(db.Boolean, nullable=False, server_default='1')
    created = db.Column(db.DateTime(), server_default=func.now())
    role = db.Column(user_types_enum, server_default='basic', nullable=False)
    pronouns = db.Column(db.String(50))

    managed_orgs = db.relationship('Org', secondary='org_manager', backref=db.backref('managers', lazy=True), lazy=True)
    _facilities = db.relationship('Facility', secondary='facility_manager',
                                  backref=db.backref('_managers', lazy=True), lazy=True)

    @property
    def managed_facilities(self):
        facilities = [f for f in self._facilities]
        for org in self.managed_orgs:
            facilities += org.facilities
        return facilities

    def password_set(self, plaintext):
        self.password = crypt.hash(plaintext)

    def password_verify(self, plaintext):
        return crypt.verify(plaintext, self.password)

    @property
    def name(self):
        name_parts = [self.given_name, self.family_name]
        return ' '.join(name_parts if self.given_name_first else name_parts[::-1])

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def gravatar(self):
        return gravatar(self.email)

    @property
    def all_tasks(self):
        role_tasks = {
            'researcher': ['edi', 'edi_extra'],
            'manager': [],
            'admin': ['author'],
            'basic': []
        }
        return ['email'] + role_tasks.get(self.role, [])

    @property
    def todo(self):
        remaining_tasks = []
        for t in self.all_tasks:
            if not getattr(self, t):
                remaining_tasks.append(t)
        return remaining_tasks

    @property
    def completion(self):
        todo = len(self.todo)
        total = len(self.all_tasks)
        if total == 0:
            return 100
        return round(((total - todo) / total) * 100)


