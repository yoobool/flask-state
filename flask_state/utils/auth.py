import logging
from werkzeug.local import LocalProxy
from flask import current_app, _request_ctx_stack


def auth():
    """
    Verify whether the user logs in through the flask-login package.
    If the user does not install flask-login, it will pass by default.
    :return: auth result: True/false
    """
    try:
        cr = current_app.login_manager
    except Exception as e:
        logging.error(e)
        return True
    current_user = LocalProxy(lambda: get_user())

    def get_user():
        if _request_ctx_stack.top is not None and not hasattr(_request_ctx_stack.top, 'user'):
            cr._load_user()
        return getattr(_request_ctx_stack.top, 'user', None)

    return current_user.is_authenticated if current_user else False
