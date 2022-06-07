# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import Facility
from ..schemas import FacilitySchema

bp = Blueprint('facility', __name__, url_prefix='/facility')


@bp.route('/')
def list_all():
    return jsonify(FacilitySchema(many=True).dump(Facility.query.all()))
