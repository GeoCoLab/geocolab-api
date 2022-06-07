# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import Slot
from ..schemas import SlotSchema

bp = Blueprint('slot', __name__, url_prefix='/slot')


@bp.route('/')
def list_all():
    return jsonify(SlotSchema(many=True).dump(Slot.query.all()))
