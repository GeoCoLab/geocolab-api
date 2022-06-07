# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from ._decorators import manager_required
from ..extensions import db
from ..models import Org
from ..schemas import OrgSchema

bp = Blueprint('org', __name__, url_prefix='/org')


@bp.route('/')
def list_all():
    return jsonify(OrgSchema(many=True).dump(Org.query.all()))


@bp.route('/new', methods=['POST'])
@manager_required()
def new():
    new_org = OrgSchema().load(request.json.get('data'))
    db.session.add(new_org)
    db.session.commit()
    return jsonify(success=True)
