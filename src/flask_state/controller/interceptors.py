# -*- encoding: utf-8 -*-
from functools import wraps

from flask import request

from ..exceptions import FlaskException
from ..exceptions.error_code import MsgCode
from ..utils.constants import HTTPStatus


def json_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method != "GET" and (
            not request.is_json or not request.get_json(silent=True)
        ):
            raise FlaskException(
                error_message=MsgCode.JSON_FORMAT_ERROR,
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return f(*args, **kwargs)

    return wrapper
