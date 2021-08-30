import json
from flask import request, abort
from functools import wraps
from jose import jwt, JWTError


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.',
            }, 401)
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
            }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found',
            }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorization header must be bearer token',
            }, 401)
    token = parts[1]
    return token


def requires_auth(page=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            check_permission(jwt, page)
            return f(jwt, *args, **kwargs)
        return wrapper
    return requires_auth_decorator


def check_permission(payload, page):
    print("Page: {}".format(page))
    
    # check if user is allowed to see the page, return true, else raise AuthError

    raise AuthError({
        'code': 'unauthorized',
        'description': 'Permission not found',
        }, 401)
    return True
