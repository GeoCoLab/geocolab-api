# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import Form, FormField, form_to_user_data
from ..schemas import FormSchema, FormFieldSchema

bp = Blueprint('forms', __name__, url_prefix='/forms')


@bp.route('/save-fields', methods=['POST'])
@jwt_required()
def save_fields():
    # TODO: admin decorator
    if current_user.role != 'admin':
        return jsonify({'error': 'Must be admin'}), 401
    fields = FormFieldSchema(many=True).load(request.json.get('fields'))
    form_name = request.json.get('form')
    form = Form.query.filter_by(name=form_name).one_or_none()
    if not form:
        return jsonify({'errors': ['Form not found.']}), 400
    form_fields = sorted(form.fields, key=lambda x: x.order)
    n_current = len(form_fields)
    n_update = len(fields)

    for i in range(max(n_current, n_update)):
        try:
            updated_field_json = fields[i]
        except IndexError:
            # doesn't exist, deleting time
            db.delete(form.fields[i])
            continue
        try:
            current_field = form_fields[i]
        except IndexError:
            # doesn't exist, make a new one
            new_field = FormField(order=i + 1, form_id=form.id, **updated_field_json)
            db.session.add(new_field)
            continue
        # they both exist! time to update
        for k, v in updated_field_json.items():
            setattr(current_field, k, v)
    db.session.commit()
    return jsonify({'success': True})


@bp.route('/<form_name>', methods=['GET'])
def view_form(form_name):
    form = Form.query.filter_by(name=form_name).one_or_none()
    if not form:
        return jsonify({'error': 'Form not found'}), 404
    return jsonify(FormSchema().dump(form))


@bp.route('/all', methods=['GET'])
def all_forms():
    forms = Form.query.all()
    if not forms:
        return jsonify({'error': 'No forms :('}), 404
    return jsonify({f.name: FormSchema().dump(f).get('fields', []) for f in forms})


@bp.route('/<form_name>', methods=['POST'])
@jwt_required()
def submit_form(form_name):
    user_data = form_to_user_data.get(form_name)
    form = Form.query.filter_by(name=form_name).one_or_none()
    if not form:
        return jsonify({'error': 'Form not found'}), 404
    form_data = request.json.get('data')
    existing_record = user_data.query.filter_by(user_id=current_user.id).one_or_none()
    if not existing_record:
        new_record = user_data(**form_data)
        new_record.user_id = current_user.id
        new_record.form_id = form.id
        db.session.add(new_record)
    else:
        for k, v in form_data.items():
            setattr(existing_record, k, v)
    db.session.commit()
    return jsonify(form_data)
