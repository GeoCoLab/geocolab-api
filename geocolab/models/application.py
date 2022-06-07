from datetime import datetime as dt

from .utils import countries_enum
from ..extensions import db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    about_request = db.Column(db.String)
    desired_location = db.Column(countries_enum)
    current_org = db.Column(db.String(200))
    additional_requirements = db.Column(db.String)
    date_from = db.Column(db.Date, nullable=False, default=dt.now().date())
    date_to = db.Column(db.Date)
    samples_estimate = db.Column(db.Integer)
    date_submitted = db.Column(db.Date)
    is_submitted = db.Column(db.Boolean, default=False, nullable=False)
    prep_required = db.Column(db.Boolean, default=True, nullable=False)
    other_analyses = db.Column(db.String)

    analyses = db.relationship('Analysis', secondary='application_analyses', lazy=True)
