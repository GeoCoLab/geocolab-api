# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify

from ..utils import countries, currencies

bp = Blueprint('misc', __name__)


@bp.route('/enum/countries', methods=['GET'])
def get_countries():
    return jsonify({k: v for k, v in countries})


@bp.route('/enum/currencies', methods=['GET'])
def get_currencies():
    return jsonify({k: v for k, v in currencies})
