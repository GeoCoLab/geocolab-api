# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import Offer
from ..schemas import OfferSchema

bp = Blueprint('offer', __name__, url_prefix='/offer')


@bp.route('/')
def list_all():
    return jsonify(OfferSchema(many=True).dump(Offer.query.all()))
