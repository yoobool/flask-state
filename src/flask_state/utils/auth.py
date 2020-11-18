from functools import wraps

from flask import _request_ctx_stack, current_app, request
from werkzeug.local import LocalProxy

from ..controller.response_methods import make_response_content
from ..exceptions import ErrorResponse
from ..exceptions.error_code import MsgCode
from ..utils.constants import HttpMethod, HTTPStatus


def auth_user(f):
    """
    Verify whether the user logs in through the flask-login package.
    If the user does not install flask-login, it will pass by default.
    :return: auth result
    :rtype: bool
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(current_app, "login_manager"):
            return f(*args, **kwargs)

        cr = current_app.login_manager
        current_user = LocalProxy(lambda: get_user())

        def get_user():
            if _request_ctx_stack.top is not None and not hasattr(_request_ctx_stack.top, "user"):
                cr._load_user()
            return getattr(_request_ctx_stack.top, "user", None)

        if not (current_user and current_user.is_authenticated):
            return make_response_content(ErrorResponse(MsgCode.AUTH_FAIL), http_status=HTTPStatus.UNAUTHORIZED)
        return f(*args, **kwargs)

    return wrapper


def auth_method(f):
    """
    Determine whether request methods is post
    :return: auth result
    :rtype: bool
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method != HttpMethod.POST.value:
            return make_response_content(
                ErrorResponse(MsgCode.REQUEST_METHOD_ERROR), http_status=HTTPStatus.METHOD_NOT_ALLOWED
            )
        return f(*args, **kwargs)

    return wrapper
