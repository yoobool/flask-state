# -*- encoding: utf-8 -*-
from functools import wraps

from flask import request

from ..controller.response_methods import make_response_content
from ..exceptions import ErrorResponse
from ..exceptions.error_code import MsgCode
from ..utils.constants import HTTPStatus


def json_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method != "GET" and (not request.is_json or not request.get_json(silent=True)):
            return make_response_content(
                resp=ErrorResponse(MsgCode.JSON_FORMAT_ERROR), http_status=HTTPStatus.BAD_REQUEST
            )
        return f(*args, **kwargs)

    return wrapper
