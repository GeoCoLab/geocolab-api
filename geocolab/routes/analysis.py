# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import Analysis
from ..schemas import AnalysisSchema

bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@bp.route('/')
def list_all():
    return jsonify(AnalysisSchema(many=True).dump(Analysis.query.all()))
