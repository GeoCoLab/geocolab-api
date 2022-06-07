# !/usr/bin/env python
# encoding: utf-8
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from flask import jsonify


def admin_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['user']['role'] == 'admin':
            return fn(*args, **kwargs)
        else:
            return jsonify(msg='No.'), 403
    return decorator


def manager_required(org=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = get_jwt_identity()
            access = False
            if org:
                access = org.can_edit(user)
            else:
                access = user.is_admin or user.role == 'manager'

            if access:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg='You do not have permission to access this.'), 403
        return decorator
    return wrapper
