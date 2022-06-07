# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return jsonify({'hello': 'it me'})
