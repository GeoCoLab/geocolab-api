# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import Application
from ..schemas import ApplicationSchema

bp = Blueprint('application', __name__, url_prefix='/application')


@bp.route('/')
def list_all():
    return jsonify(ApplicationSchema(many=True).dump(Application.query.all()))
