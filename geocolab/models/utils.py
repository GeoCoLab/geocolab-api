from ..extensions import db
from ..utils import countries
import hashlib


countries_enum = db.Enum(*[c[0] for c in countries], name='countries')

user_types_enum = db.Enum('manager', 'admin', 'researcher', name='user_types')


def gravatar(email):
    email_hash = hashlib.md5(email.encode().lower()).hexdigest()
    url = f'https://gravatar.com/avatar/{email_hash}?d=robohash'
    return url
