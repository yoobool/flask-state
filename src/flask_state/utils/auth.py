from functools import wraps

from flask import _request_ctx_stack, current_app
from werkzeug.local import LocalProxy

from ..exceptions import FlaskException
from ..exceptions.error_code import MsgCode
from ..utils.constants import HTTPStatus


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
            if _request_ctx_stack.top is not None and not hasattr(
                _request_ctx_stack.top, "user"
            ):
                cr._load_user()
            return getattr(_request_ctx_stack.top, "user", None)

        if not (current_user and current_user.is_authenticated):
            raise FlaskException(
                error_message=MsgCode.AUTH_FAIL,
                status_code=HTTPStatus.UNAUTHORIZED,
            )
        return f(*args, **kwargs)

    return wrapper
