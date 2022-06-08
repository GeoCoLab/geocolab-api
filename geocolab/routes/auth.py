# !/usr/bin/env python
# encoding: utf-8

from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, create_access_token, set_access_cookies, jwt_required, \
    unset_jwt_cookies, create_refresh_token, set_refresh_cookies

from ..extensions import jwt_manager, db
from ..models import User
from ._decorators import admin_required
from ..schemas import UserSchema

bp = Blueprint('auth', __name__)


def login_user(user_object, remember=False):
    """
    Shared method between login and register.
    """
    user_dict = UserSchema().dump(user_object)
    access_token = create_access_token(identity=user_object, additional_claims={'user': user_dict})
    refresh_exp = timedelta(days=28) if remember else timedelta(hours=1)
    refresh_token = create_refresh_token(identity=user_object, expires_delta=refresh_exp)
    response = jsonify(user_dict)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@jwt_manager.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt_manager.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.get(identity)


@bp.route('/csrf', methods=['GET'])
def refresh_csrf():
    return jsonify('')


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_jwt():
    identity = current_user
    access_token = create_access_token(identity=identity)
    response = jsonify(access_token=access_token)
    set_access_cookies(response, access_token)
    return response


@bp.route('/user')
@jwt_required()
def get_user():
    return jsonify(UserSchema().dump(current_user))


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
