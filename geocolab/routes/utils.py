# !/usr/bin/env python
# encoding: utf-8

from datetime import datetime as dt, timedelta, timezone

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, create_access_token, get_jwt_identity, \
    set_access_cookies, create_refresh_token, set_refresh_cookies, get_jwt_header
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import ExpiredSignatureError

from ..models import User
from ..schemas import UserSchema


def nearly_expired(token):
    exp_timestamp = token['exp']
    target_timestamp = dt.timestamp(dt.now(timezone.utc) + timedelta(minutes=30))
    return target_timestamp > exp_timestamp


def should_remember(token_header):
    return token_header.get('additional_claims', {}).get('remember', False)


def refresh_expiring_jwts(response):
    refresh_token = False
    identity = None
    remember = False
    create_refresh_tokens = False
    try:
        try:
            # check for access token
            verify_jwt_in_request()
            identity = User.query.get(get_jwt_identity())
            remember = should_remember(get_jwt_header())
            create_refresh_tokens = True
            if nearly_expired(get_jwt()):
                # nearly expired, needs refreshing
                refresh_token = True
        except (ExpiredSignatureError, NoAuthorizationError):
            # no valid access token, check for a refresh token
            try:
                verify_jwt_in_request(refresh=True)
                identity = User.query.get(get_jwt_identity())
                remember = True
                refresh_token = True
            except (ExpiredSignatureError, NoAuthorizationError):
                # no valid refresh token either
                raise DoubleExpired
    except DoubleExpired:
        return response
    if refresh_token:
        # either there's a nearly-expired access token or there's a refresh token
        response = login_user(identity, remember, response, create_refresh_tokens)
    return response


class DoubleExpired(Exception):
    pass


def login_user(user_object, remember=False, response=None, create_refresh_tokens=False):
    """
    Shared method between login, register, and refresh_jwt.
    """
    user_dict = UserSchema().dump(user_object)
    response = response or jsonify(user_dict)
    access_token = create_access_token(identity=user_object,
                                       additional_claims={'user': user_dict, 'remember': remember})
    set_access_cookies(response, access_token)
    if remember and create_refresh_tokens:
        refresh_token = create_refresh_token(identity=user_object, expires_delta=timedelta(days=365))
        set_refresh_cookies(response, refresh_token, max_age=timedelta(days=365).total_seconds())
    return response
