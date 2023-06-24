# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user

from ._decorators import manager_required
from ..extensions import db
from ..models import Facility
from ..schemas import FacilitySchema

bp = Blueprint('facility', __name__, url_prefix='/facility')


@bp.route('/all')
@manager_required()
def list_all():
    if current_user.is_admin:
        all_facilities = Facility.query.all()
    else:
        all_facilities = current_user.facilities
    return jsonify(FacilitySchema(many=True).dump(all_facilities))


@bp.route('/<facility_id>')
@manager_required()
def get_facility_by_id(facility_id):
    facility = Facility.query.get(facility_id)
    if not facility and current_user.is_admin:
        return jsonify({'error': 'Facility not found.'}), 404
    elif not facility or not facility.can_edit(current_user):
        return jsonify({'error': 'Either does not exist or you do not have access.'}), 401
    return jsonify(FacilitySchema().dump(facility))


@bp.route('/save', methods=['POST'])
@manager_required()
def save():
    facility_dict = FacilitySchema().load(request.json)
    if facility_dict.get('id'):
        facility = Facility.query.get(facility_dict.get('id'))
        for k, v in facility_dict.items():
            setattr(facility, k, v)
    else:
        facility = Facility(**facility_dict)
        facility._managers.append(current_user)
    db.session.add(facility)
    db.session.commit()
    return jsonify(FacilitySchema().dump(facility))
