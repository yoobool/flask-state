from flask import jsonify, make_response


def make_response_content(resp, msg=None, http_status=200):
    """
    Construct response
    :param resp: response class
    :param msg: response msg
    :param http_status: HTTP Status Code
    :return: flask response
    """
    if not msg:
        msg = resp.get_msg()
    code = resp.get_code()
    data = resp.get_data()
    response = make_response(jsonify(code=code, msg=msg, data=data), http_status)
    return response
