# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from ._decorators import manager_required
from ..extensions import db
from ..models import Org
from ..schemas import OrgSchema

bp = Blueprint('org', __name__, url_prefix='/org')


@bp.route('/all')
@manager_required()
def list_all():
    if current_user.is_admin:
        all_orgs = Org.query.all()
    else:
        all_orgs = current_user.orgs
    return jsonify(OrgSchema(many=True).dump(all_orgs))


@bp.route('/<org_id>')
@manager_required()
def get_org_by_id(org_id):
    org = Org.query.get(org_id)
    if not org and current_user.is_admin:
        return jsonify({'error': 'Organisation/Institution not found.'}), 404
    elif not org or not org.can_edit(current_user):
        return jsonify({'error': 'Either does not exist or you do not have access.'}), 401
    return jsonify(OrgSchema().dump(org))


@bp.route('/save', methods=['POST'])
@manager_required()
def save():
    org_dict = OrgSchema().load(request.json)
    if org_dict.get('id'):
        org = Org.query.get(org_dict.get('id'))
        for k, v in org_dict.items():
            setattr(org, k, v)
    else:
        org = Org(**org_dict)
        org.managers.append(current_user)
    db.session.add(org)
    db.session.commit()
    return jsonify(OrgSchema().dump(org))
