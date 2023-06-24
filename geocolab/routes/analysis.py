# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify

from ..models import Analysis
from ..schemas import AnalysisSchema, NestedAnalysisSchema

bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@bp.route('/flat')
def list_flat():
    return jsonify(AnalysisSchema(many=True).dump(Analysis.query.all()))


@bp.route('/nested')
def list_nested():
    return jsonify(NestedAnalysisSchema(many=True).dump(Analysis.query.filter(Analysis.parent_id.is_(None)).all()))
