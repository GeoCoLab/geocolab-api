# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required, \
    unset_jwt_cookies

from ._decorators import admin_required
from .utils import login_user, refresh_expiring_jwts
from ..extensions import jwt_manager, db
from ..models import User, Secret
from ..schemas import UserSchema
import json

bp = Blueprint('auth', __name__)


@jwt_manager.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt_manager.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.get(identity)


@bp.route('/user')
@jwt_required(optional=True)
def get_user():
    logged_in = current_user is None
    response = jsonify({})
    if not logged_in:
        response = refresh_expiring_jwts(response)
    response.set_data(json.dumps(UserSchema().dump(current_user)))
    return response


@bp.route('/user/<user_id>')
@admin_required
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return jsonify(UserSchema().dump(user))


@bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    remember = request.json.get('remember')
    usr = User.query.filter_by(email=email).one_or_none()
    if not usr:
        return jsonify({'errors': ['User does not exist']}), 401
    if not usr.password_verify(password):
        return jsonify({'errors': ['Incorrect password']}), 401
    return login_user(usr, remember)


@bp.route("/logout", methods=['POST'])
def logout():
    response = jsonify({'msg': 'logout successful'})
    unset_jwt_cookies(response)
    return response


@bp.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    if User.query.filter_by(email=email).one_or_none():
        return jsonify({'errors': ['Email address already in use.']}), 401
    user_dict = UserSchema().load(request.json)
    new_user = User(**user_dict)
    password = request.json.get('password')
    new_user.password_set(password)
    db.session.add(new_user)
    db.session.commit()
    return login_user(new_user)


@bp.route('/knock-knock', methods=['POST'])
@jwt_required()
def knock_knock():
    """
    Changes a user to admin if they provide the secret password.
    """
    password = request.json.get('password')
    secret = Secret.query.get('knockknock')
    if current_user.is_admin:
        if not secret:
            secret = Secret(key='knockknock')
            db.session.add(secret)
        secret.value_set(password)
        return jsonify('Successfully set new passcode.')
    if not secret:
        return jsonify({'errors': ['No idea what this is but it hasn\'t been set up yet, sorry.']}), 401
    if secret.value_verify(password):
        current_user.role = 'admin'
        db.session.commit()
        return jsonify('Excellent.')
    return jsonify({'errors': [f'I have no idea who this "{password}" is, but I think you have the wrong door.']}), 401

