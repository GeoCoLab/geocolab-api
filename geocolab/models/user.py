from sqlalchemy.sql import func

from .utils import countries_enum, user_types_enum, gravatar
from ..extensions import db, crypt

role_tasks = {
    'researcher': ['edi', 'edi_extra'],
    'manager': [],
    'admin': []
}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    given_name_first = db.Column(db.Boolean, nullable=False, server_default='1')
    created = db.Column(db.DateTime(), server_default=func.now())
    country = db.Column(countries_enum)
    role = db.Column(user_types_enum, server_default='researcher')
    pronouns = db.Column(db.String(50))

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
    def todo(self):
        remaining_tasks = []
        for t in role_tasks.get(self.role, []):
            if not getattr(self, t):
                remaining_tasks.append(t)
        return remaining_tasks

    @property
    def completion(self):
        todo = len(self.todo)
        total = len(role_tasks.get(self.role, []))
        if total == 0:
            return 100
        return round((todo/total)*100)
