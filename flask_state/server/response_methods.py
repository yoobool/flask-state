from flask import make_response, jsonify
from . import MsgCode


def make_response_content(resp=MsgCode.SUCCESS, msg=None, data=None):
    """
    Construct response
    :param resp: response.code
    :param msg: response.msg
    :param data: response.data
    :return: flask response
    """
    if not msg:
        msg = resp.get_msg()
    code = resp.get_code()
    response = make_response(jsonify(code=code, msg=msg, data=data))
    return response
