from flask import make_response, jsonify
from ..exceptions import SuccessResponse


def make_response_content(resp, msg=None):
    """
    Construct response
    :param resp: response class
    :param msg: response msg
    :return: flask response
    """
    if not msg:
        msg = resp.get_msg()
    code = resp.get_code()
    data = resp.get_data()
    response = make_response(jsonify(code=code, msg=msg, data=data))
    return response
