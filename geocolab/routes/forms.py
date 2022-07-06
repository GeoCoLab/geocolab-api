# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import form_to_user_data

bp = Blueprint('forms', __name__, url_prefix='/forms')


@bp.route('/<form_name>', methods=['POST'])
@jwt_required()
def submit_form(form_name):
    user_data = form_to_user_data.get(form_name)
    if not user_data:
        return jsonify({'error': 'Form not found'}), 404
    form_data = request.json.get('data')
    existing_record = user_data.query.filter_by(user_id=current_user.id).one_or_none()
    if not existing_record:
        new_record = user_data(**form_data)
        new_record.user_id = current_user.id
        db.session.add(new_record)
    else:
        for k, v in form_data.items():
            setattr(existing_record, k, v)
    db.session.commit()
    return jsonify(form_data)
